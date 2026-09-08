# AI-Based E-Commerce Product Profitability & Business Decision Intelligence System (Research Edition)

A production-grade, research-validated Machine Learning and Prescriptive Business Decision Intelligence System designed to predict e-commerce product profitability, quantify prediction uncertainty, optimize commercial pricing/discount strategies, and evaluate decision frameworks.

---

## 🌟 Research Enhancements & Key Features

### 1. Split Conformal Prediction Uncertainty Estimation
- **Methodology**: Non-parametric Split Conformal Prediction based on empirical validation residuals.
- **Coverage**: Computes 90% Conformal Prediction Intervals for **Demand**, **Revenue**, and **Profit**.
- **Metrics**: Evaluates Prediction Interval Coverage Probability (**PICP**) and Mean Prediction Interval Width (**MPIW**).
- **Downside Risk**: Calculates empirical probability of operating loss $P(\text{Profit} < 0)$ and Expected Downside Loss.

### 2. Prescriptive Business Optimization
- **Price Optimization**: Dynamic optimal price search space with risk constraints.
- **Discount Optimization**: Evaluates promotional discount curves ($0\%$ to $80\%$).
- **Advertising Optimization**: Analyzes ROI against incremental profit.
- **Optimization Objectives**: Maximize Expected Profit, Maximize Revenue, Maximize Profit Margin, Maximize Business Score.

### 3. Baseline vs. Proposed Framework Comparison
- **Baseline Framework**: Direct Profit Prediction + Linear Regression + Simple Rule-Based Decision ($Profit > 0$).
- **Proposed Framework**: Multi-Stage Demand Decomposition $\rightarrow$ Revenue Estimation $\rightarrow$ Profit Estimation $\rightarrow$ Conformal Uncertainty $\rightarrow$ Risk Engine $\rightarrow$ Prescriptive Optimization $\rightarrow$ SHAP Explainability.
- **Hypothesis Testing**: Infrastructure for empirical validation of Hypotheses H1, H2, H3, H4.

### 4. Ablation Study
- Evaluates 6 distinct configurations (Full Framework, Without Risk, Without Uncertainty, Without Optimization, Without SHAP, Without Demand Decomposition).
- Saves research artifacts automatically to `research_results/` (`baseline_results.csv`, `ablation_results.csv`, `model_comparison.csv`, `data_quality_report.json`).

### 5. Real-World & Synthetic Dataset Support
- **Primary Real Dataset**: `data/ecommerce_sales_dataset.csv` (10,000 real transaction records).
- **Schema Validation & Quality**: Automatic column mapping, leakage detection, and Data Quality Score computation.

---

## 🛠️ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Models & Prepare Conformal Pipeline
```bash
python -m src.train_models
```

### 3. Run Research Baseline & Ablation Experiments
```bash
python -m research.baseline
python -m research.ablation
```

### 4. Launch Streamlit Application
```bash
streamlit run app.py
```

---

## 📐 System Architecture & Module Structure

```
ecommerce_profitability_system/
├── app.py                      # Main Streamlit Application (Multi-Page & Research Tabs)
├── requirements.txt            # Python dependencies
├── README.md                   # Complete research documentation
├── data/
│   ├── ecommerce_sales_dataset.csv # Primary 10,000 transaction dataset
│   ├── prediction_history.json # Local analysis record log
│   └── README.md               # Dataset documentation
├── models/
│   ├── preprocessing_pipeline.pkl
│   ├── best_demand_model.pkl
│   ├── best_profit_model.pkl
│   ├── model_metrics.json
│   └── conformal_quantiles.json# Empirical residual quantiles
├── src/
│   ├── data_loader.py          # Data loading & quality score computation
│   ├── preprocessing.py        # Sklearn preprocessing pipeline
│   ├── feature_engineering.py  # Engineered features & pre-launch safety
│   ├── evaluate_models.py      # Metric calculation (R2, MAE, RMSE, MAPE)
│   ├── train_models.py         # 6-Model training & conformal quantile calculation
│   ├── prediction.py           # Product analysis & conformal interval estimation
│   ├── uncertainty.py          # Split conformal prediction & loss probability P(Profit < 0)
│   ├── optimization.py         # Prescriptive Price, Discount, and Advertising Optimizer
│   ├── risk_engine.py          # Multi-factor risk engine incorporating uncertainty
│   ├── business_score.py       # 0–100 business scoring engine
│   ├── launch_decision.py      # Decision engine (LAUNCH / MODIFY / REJECT)
│   ├── recommendation_engine.py# Actionable recommendations & executive conclusion
│   ├── explainability.py       # SHAP Feature Importance & Local Explanation
│   └── ui/                     # UI components, charts, styles, and page layouts
├── research/
│   ├── baseline.py             # Baseline vs Proposed Framework evaluation
│   ├── ablation.py             # 6-Experiment Ablation Study & Hypothesis Testing
│   └── experiment_tracker.py   # Reproducible experiment logging system
└── research_results/           # Exported CSVs and JSON research artifacts
```
