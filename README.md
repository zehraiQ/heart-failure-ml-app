# Heart Failure Risk Prediction — Full-Stack ML Web App

A Django web application that predicts mortality risk in heart failure patients using machine learning. Includes data analysis with Jupyter notebooks, trained ML models, and a full clinic management system.

## Features

- **ML Models:** Decision Tree, KNN, Naive Bayes, Random Forest, Logistic Regression
- **Preprocessing:** SMOTE for class imbalance, outlier detection, feature scaling
- **Web App:** Patient management, appointment scheduling, risk prediction dashboard
- **Dockerized:** Easy deployment with docker-compose

## Tech Stack

- **Backend:** Django 5, scikit-learn, pandas, joblib
- **Frontend:** HTML5, CSS3, Bootstrap-style templates
- **DevOps:** Docker, Gunicorn

## Project Structure

```
Backend/              — Django web application
  kalp_yetmezligi/    — Core Django settings
  klinik/             — Clinic app (models, views, forms)
  ai_entegrasyon.py   — ML model integration
Frontend/             — HTML templates
YapayZeka_Modulu/     — Trained ML models (.pkl) + training script
figures/              — Generated visualizations
```

## Quick Start

```bash
# Using Docker
docker-compose up

# Or manually
pip install -r requirements.txt
python Backend/manage.py migrate
python Backend/manage.py runserver
```

## Dataset

UCI Heart Failure Clinical Records — 299 patients, 12 clinical features (age, ejection fraction, serum creatinine, etc.).
