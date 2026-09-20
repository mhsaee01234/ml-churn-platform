# ML Churn Prediction Platform

A production-style machine learning platform for predicting customer churn using a trained ML model, FastAPI, PostgreSQL, JWT authentication, Docker, Prometheus, Grafana, GitHub Actions, and Render.

## 🚀 Live Demo

**API:** https://ml-churn-platform.onrender.com

**Swagger Documentation:** https://ml-churn-platform.onrender.com/docs

---

## 📌 Project Overview

The ML Churn Prediction Platform provides an API for predicting whether a customer is likely to churn.

The platform includes:

- Machine Learning prediction
- FastAPI REST API
- JWT-based authentication
- PostgreSQL database
- Prediction history
- Docker containerization
- Docker Compose
- Prometheus monitoring
- Grafana dashboard
- Automated testing with Pytest
- GitHub Actions CI
- Cloud deployment using Render

---

## 🏗️ Architecture

```text
                    Customer
                       |
                       v
                +--------------+
                |   FastAPI    |
                |     API      |
                +--------------+
                       |
              JWT Authentication
                       |
                       v
                +--------------+
                | ML Prediction|
                |    Model     |
                +--------------+
                       |
                       v
                +--------------+
                | PostgreSQL   |
                |  Database    |
                +--------------+
                       |
                       v
              Prediction History


        Monitoring
            |
            v
      +------------+
      | Prometheus |
      +------------+
            |
            v
       +---------+
       | Grafana |
       +---------+

CI/CD:
GitHub → GitHub Actions → Docker → Render