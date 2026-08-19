# AI-Based E-Commerce Product Profitability & Business Decision Intelligence System

A production-ready, modular Machine Learning and Business Decision Intelligence application for Indian E-Commerce businesses to estimate demand, revenue, profit, risk, and business viability before product launch or campaign promotion.

## Features

- **Synthetic Realistic Dataset (25,000 Records)**: Indian e-commerce context (Amazon, Flipkart, Meesho, Myntra, Snapdeal), seasonal events (Diwali, Holi, Navratri, etc.), categories, regions, pricing, return rates, rating, and competition.
- **6 Machine Learning Regression Models**:
  1. Multiple Linear Regression
  2. Random Forest Regressor
  3. XGBoost Regressor
  4. LightGBM Regressor
  5. CatBoost Regressor
  6. Deep Feedforward Neural Network (ANN / Keras / MLPRegressor)
- **Dynamic Evaluation**: Real evaluation on Validation & Test split ($R^2$, MAE, RMSE, MAPE). Zero hardcoding!
- **Business Intelligence Engines**:
  - **Dynamic Multi-Factor Risk Engine**: Low, Medium, High risk output with specific positive/negative risk drivers.
  - **Dynamic 0–100 Business Score**: Weighted profitability, demand, ROAS, operational risk, and model metrics.
  - **Launch Decision Engine**: 🟢 LAUNCH, 🟡 LAUNCH WITH MODIFICATIONS, 🔴 DO NOT LAUNCH.
  - **Actionable Recommendation Engine**: Custom contextual business advice.
  - **Automated Conclusion**: Concise natural language synthesis.
- **Explainable AI (SHAP)**: Global feature importance, local prediction explanations, and permutation fallbacks.
- **What-If Business Simulator**: Dynamic scenario testing with side-by-side metric deltas.
- **Prediction History**: Local run persistence and export.

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Models & Prepare Pipeline
```bash
python src/train_models.py
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```

## System Architecture

```
ecommerce_profitability_system/
├── app.py                      # Main Streamlit Application UI
├── requirements.txt            # System dependencies
├── README.md                   # System documentation
├── data/
│   ├── ecommerce_data.csv      # Generated dataset
│   └── prediction_history.json # Local analysis log
├── models/
│   ├── preprocessing_pipeline.pkl
│   ├── best_demand_model.pkl
│   ├── best_profit_model.pkl
│   ├── model_metrics.json
│   ├── all_demand_models.pkl
│   └── all_profit_models.pkl
├── src/
│   ├── data_loader.py          # Data generation & schema validation
│   ├── preprocessing.py        # Preprocessing & pipeline creation
│   ├── feature_engineering.py  # Feature transformations
│   ├── evaluate_models.py      # Metrics computation
│   ├── train_models.py         # End-to-end model training script
│   ├── prediction.py           # Single product prediction & financial calculations
│   ├── risk_engine.py          # Dynamic risk analysis
│   ├── business_score.py       # 0–100 business scoring engine
│   ├── launch_decision.py      # Decision engine
│   ├── recommendation_engine.py# Recommendations generator
│   └── explainability.py       # SHAP and Permutation importance
└── utils/
    └── helpers.py              # Formatting (₹), logging, and persistence
```
