from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    feature_1 = Column(Float)
    feature_2 = Column(Float)
    feature_3 = Column(Float)
    prediction = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)