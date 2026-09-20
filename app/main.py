from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, field_validator
import joblib
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app import models
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


app = FastAPI(title="ML Churn Prediction API")

security = HTTPBearer()

# Prometheus monitoring
Instrumentator().instrument(app).expose(app)


# Create database tables
Base.metadata.create_all(bind=engine)


# Load trained ML model
model = joblib.load("ml/churn_model.pkl")


# -------------------------
# Request Models
# -------------------------

class CustomerData(BaseModel):
    features: list[float]

    @field_validator("features")
    @classmethod
    def validate_features(cls, value):
        if len(value) != 3:
            raise ValueError("Exactly 3 features are required.")
        return value


class UserCreate(BaseModel):
    username: str
    password: str


# -------------------------
# Database Dependency
# -------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# -------------------------
# Authentication Dependency
# -------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return verify_token(credentials.credentials)


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "ML Churn Prediction API is running!"
    }


# -------------------------
# Register
# -------------------------

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully.",
        "user_id": new_user.id
    }


# -------------------------
# Login
# -------------------------

@app.post("/login")
def login(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    token = create_access_token(
        {"sub": existing_user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
# Prediction
# -------------------------

@app.post("/predict")
def predict(
    customer: CustomerData,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    prediction = model.predict([customer.features])

    result = models.Prediction(
        feature_1=customer.features[0],
        feature_2=customer.features[1],
        feature_3=customer.features[2],
        prediction=int(prediction[0])
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "prediction": int(prediction[0]),
        "saved_id": result.id
    }


# -------------------------
# Prediction History
# -------------------------

@app.get("/predictions")
def get_predictions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    predictions = db.query(models.Prediction).all()

    return [
        {
            "id": item.id,
            "feature_1": item.feature_1,
            "feature_2": item.feature_2,
            "feature_3": item.feature_3,
            "prediction": item.prediction
        }
        for item in predictions
    ]