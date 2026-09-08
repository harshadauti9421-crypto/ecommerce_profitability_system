# E-Commerce Profitability AI — Dataset Documentation

## Overview
This repository supports both real-world e-commerce datasets and synthetic datasets for research, model training, and business decision intelligence evaluation.

---

## Supported Datasets

### 1. Primary Real-World E-Commerce Sales Dataset (`data/ecommerce_sales_dataset.csv`)
- **Format**: CSV (`.csv`)
- **Total Records**: 10,000 transaction records
- **Total Columns**: 26 raw features
- **Features**: Order_ID, Order_Date, Year, Month, Quarter, Season, Customer_ID, Customer_Gender, Customer_Segment, Region, Country, Category, Sub_Category, Product_Name, Unit_Price, Quantity, Discount, Revenue, Cost, Profit, Profit_Margin_%, Shipping_Cost, Shipping_Method, Shipping_Days, Payment_Method, Order_Status.
- **Usage**: Primary dataset for model training, conformal prediction interval calibration, baseline comparison, and ablation experiments.

### 2. Secondary Real-World Dataset (`data/raw/global_superstore_2016.xlsx`)
- **Format**: Excel Workbook (`.xlsx`)
- **Total Records**: 51,290 records across global markets.

---

## Data Leakage Prevention Protocol
To guarantee strict pre-launch research integrity:
- Models are trained strictly on pre-launch available attributes (`selling_price`, `cost_price`, `discount_percent`, `shipping_cost`, `product_category`, `product_subcategory`, `region`, `season`, `payment_method`).
- Post-launch outcomes (`actual revenue`, `actual profit`) are separated as ground-truth targets only.

---

## Feature Mapping & Normalization
The `src/data_loader.py` module automatically standardizes variable names across datasets:
- `Revenue` $\rightarrow$ `sales`
- `Unit_Price` $\rightarrow$ `selling_price`
- `Cost` $\rightarrow$ `cost_price`
- `Discount` $\rightarrow$ `discount_percent` (0%–100%)
- `Quantity` $\rightarrow$ `demand` target
- `Profit` $\rightarrow$ `profit` target
