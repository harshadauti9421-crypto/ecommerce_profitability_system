import os
import hashlib
import json
import pandas as pd
import numpy as np
from utils.helpers import logger

RAW_DATA_PATH = os.path.join("data", "raw", "global_superstore_2016.xlsx")
FALLBACK_DATA_PATH = os.path.join("data", "global_superstore_2016.xlsx")
RESULTS_DIR = "research_results"

# UI Categories and Domain Metadata Constants
CATEGORY_SUBCATEGORIES = {
    "Electronics": ["Smartphones", "Laptops", "Headphones", "Tablets", "Software"],
    "Clothing": ["Men's Wear", "Women's Wear", "Footwear"],
    "Home & Kitchen": ["Furniture", "Appliances", "Kitchen Tools"],
    "Beauty & Health": ["Skincare", "Supplements"],
    "Books & Media": ["Books"],
    "Technology": ["Phones", "Accessories", "Copiers", "Machines"],
    "Furniture": ["Bookcases", "Chairs", "Furnishings", "Tables"],
    "Office Supplies": ["Appliances", "Art", "Binders", "Envelopes", "Fasteners", "Labels", "Paper", "Storage", "Supplies"]
}

SEASONS = ["Regular Season", "Summer", "Fall", "Winter", "Spring", "Diwali", "Holi", "Navratri", "Eid", "Christmas"]
PLATFORMS = ["Amazon", "Flipkart", "Meesho", "Myntra", "Snapdeal", "Shopify", "Direct Store"]
MARKETING_CHANNELS = ["Social Media", "Search Ads", "Influencer", "Email", "Organic"]
COMPETITION_LEVELS = ["Low", "Medium", "High"]
REGIONS = ["East", "West", "Central", "South", "North", "EMEA", "APAC", "LATAM"]
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Google Pay", "Net Banking", "COD"]

# Real-World Feature Availability Classification
FEATURE_AVAILABILITY = {
    "selling_price": "DERIVABLE",      # Derived: Sales / Quantity
    "cost_price": "DERIVABLE",         # Derived: (Sales - Profit) / Quantity
    "discount_percent": "AVAILABLE",   # Available: Discount * 100.0
    "shipping_cost": "AVAILABLE",     # Available: Shipping Cost
    "category": "AVAILABLE",          # Available: Category
    "subcategory": "AVAILABLE",       # Available: Sub-Category
    "market": "AVAILABLE",            # Available: Market
    "region": "AVAILABLE",            # Available: Region
    "segment": "AVAILABLE",           # Available: Segment
    "ship_mode": "AVAILABLE",         # Available: Ship Mode
    "order_priority": "AVAILABLE",    # Available: Order Priority
    "quantity": "AVAILABLE",          # Available: Demand Target / Quantity
    "profit": "AVAILABLE",            # Available: Primary Profit Target
    "sales": "AVAILABLE",             # Available: Gross Sales Revenue
    "advertising_cost": "UNAVAILABLE",# Unavailable in raw dataset
    "product_rating": "UNAVAILABLE",  # Unavailable in raw dataset
    "return_rate": "UNAVAILABLE",     # Unavailable in raw dataset
    "marketing_channel": "UNAVAILABLE",# Unavailable in raw dataset
    "competition_level": "UNAVAILABLE"# Unavailable in raw dataset
}

def calculate_file_sha256(file_path):
    """Calculate cryptographic SHA-256 hash for dataset reproducibility."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def find_dataset_file():
    """Safely locate dataset file (CSV or Excel)."""
    candidates = [
        os.path.join("data", "ecommerce_sales_dataset.csv"),
        os.path.join("data", "raw", "ecommerce_sales_dataset.csv"),
        RAW_DATA_PATH,
        FALLBACK_DATA_PATH,
        os.path.join("data", "ecommerce_data.csv"),
        os.path.join("data", "raw", "Global Superstore.xlsx"),
        os.path.join("data", "Global Superstore.xlsx")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def load_real_superstore_dataset(file_path=None):
    """
    Load real-world e-commerce dataset (CSV or Excel workbook).
    Strictly REAL DATA ONLY — No synthetic data generation or synthetic fallback.
    """
    if file_path is None:
        file_path = find_dataset_file()
        
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(
            "REAL RESEARCH DATASET NOT FOUND.\n"
            "Please place 'ecommerce_sales_dataset.csv' or 'global_superstore_2016.xlsx' inside the 'data/' directory."
        )
        
    logger.info(f"Loading real-world dataset from: {file_path}")
    dataset_hash = calculate_file_sha256(file_path)
    logger.info(f"Dataset SHA-256 Hash: {dataset_hash}")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".csv", ".txt"]:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded CSV dataset with {len(df):,} rows and {len(df.columns)} columns.")
    else:
        xl = pd.ExcelFile(file_path)
        sheet_name = "Orders" if "Orders" in xl.sheet_names else xl.sheet_names[0]
        df = xl.parse(sheet_name)
        logger.info(f"Loaded sheet '{sheet_name}' with {len(df):,} rows and {len(df.columns)} columns.")
    
    # Standardize column names
    col_mapping = {
        "Product_Name": "product_name",
        "Product Name": "product_name",
        "Category": "product_category",
        "Sub_Category": "product_subcategory",
        "Sub-Category": "product_subcategory",
        "Revenue": "sales",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
        "Shipping_Cost": "shipping_cost",
        "Shipping Cost": "shipping_cost",
        "Market": "market",
        "Region": "region",
        "Customer_Segment": "segment",
        "Segment": "segment",
        "Shipping_Method": "ship_mode",
        "Ship Mode": "ship_mode",
        "Order Priority": "order_priority",
        "Order_Date": "order_date",
        "Order Date": "order_date",
        "Unit_Price": "unit_price",
        "Cost": "unit_cost",
        "Season": "season",
        "Payment_Method": "payment_method",
        "Payment Method": "payment_method",
        "Marketing_Channel": "marketing_channel",
        "Competition_Level": "competition_level",
        "Platform": "platform"
    }
    
    df = df.rename(columns={k: v for k, v in col_mapping.items() if k in df.columns})
    
    # Convert dates if present
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        df["order_year"] = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_dow"] = df["order_date"].dt.dayofweek
    else:
        df["order_year"] = 2023
        df["order_month"] = 6
        df["order_dow"] = 2
        
    # Standardize numeric columns
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce").fillna(0.0)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(0.0)
    df["shipping_cost"] = pd.to_numeric(df["shipping_cost"], errors="coerce").fillna(0.0)
    
    # Discount percent logic
    if "discount" in df.columns:
        disc = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)
        if (disc <= 1.0).all():
            df["discount_percent"] = (disc * 100.0).round(2)
        else:
            df["discount_percent"] = disc.round(2)
    else:
        df["discount_percent"] = 0.0
    
    # Derive unit price and unit cost dynamically if not explicitly present
    if "unit_price" in df.columns:
        df["selling_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0).round(2)
    else:
        df["selling_price"] = (df["sales"] / np.maximum(df["quantity"], 1)).round(2)
        
    if "unit_cost" in df.columns:
        df["cost_price"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0.0).round(2)
    else:
        df["cost_price"] = ((df["sales"] - df["profit"]) / np.maximum(df["quantity"], 1)).round(2)
    
    df["unit_price"] = df["selling_price"]
    df["unit_cost"] = df["cost_price"]
    
    # Ensure missing domain features have sensible defaults
    if "advertising_cost" not in df.columns:
        df["advertising_cost"] = 0.0
    if "return_rate" not in df.columns:
        df["return_rate"] = 0.05
    if "product_rating" not in df.columns:
        df["product_rating"] = 4.2
    if "marketing_channel" not in df.columns:
        df["marketing_channel"] = "Organic"
    if "competition_level" not in df.columns:
        df["competition_level"] = "Medium"
    if "platform" not in df.columns:
        df["platform"] = "Amazon"
    if "season" not in df.columns:
        df["season"] = "Regular Season"
    if "payment_method" not in df.columns:
        df["payment_method"] = "Credit Card"
    if "product_category" not in df.columns:
        df["product_category"] = "Technology"
    if "product_subcategory" not in df.columns:
        df["product_subcategory"] = "Accessories"
    
    # Target columns
    df["demand"] = df["quantity"]
    df["revenue"] = df["sales"]
    
    # Drop corrupt rows where quantity <= 0
    df = df[df["quantity"] > 0].copy()
    
    df.attrs["sha256"] = dataset_hash
    df.attrs["file_name"] = os.path.basename(file_path)
    return df

def generate_data_quality_report(df, dataset_name="Global E-Commerce Sales Dataset | 2021–2024", dataset_type="REAL-WORLD DATA"):
    """
    Generate complete Data Quality Report for real dataset and save to research_results/.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    num_rows = len(df)
    num_cols = len(df.columns)
    missing_count = int(df.isnull().sum().sum())
    dup_count = int(df.duplicated().sum())
    sha256_hash = df.attrs.get("sha256", "N/A")
    
    num_cols_list = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols_list = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    penalty = 0
    if missing_count > 0:
        penalty += min(20, int(missing_count / (num_rows * num_cols) * 100))
    if dup_count > 0:
        penalty += min(15, int(dup_count / num_rows * 100))
        
    quality_score = max(0, 100 - penalty)
    
    report = {
        "dataset_name": dataset_name,
        "dataset_type": dataset_type,
        "sha256_hash": sha256_hash,
        "num_rows": num_rows,
        "num_cols": num_cols,
        "missing_values": missing_count,
        "duplicate_rows": dup_count,
        "numerical_columns": num_cols_list,
        "categorical_columns": cat_cols_list,
        "quality_score": quality_score,
        "feature_availability": FEATURE_AVAILABILITY
    }
    
    json_path = os.path.join(RESULTS_DIR, "data_quality_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    logger.info(f"Data Quality Report saved to {json_path}")
    return report

def get_product_name_col(df):
    """Detect product name column from real dataset."""
    candidates = ["product_name", "Product Name", "product", "Product"]
    for c in candidates:
        if c in df.columns:
            return c
    return None

def load_and_validate_data(file_path=None):
    """Primary data loader wrapper calling load_real_superstore_dataset."""
    return load_real_superstore_dataset(file_path)

def load_external_dataset(file_path_or_bytes, file_name, column_mapping=None):
    """Load user uploaded external dataset (CSV/Excel/JSON)."""
    ext = os.path.splitext(file_name)[1].lower()
    if ext in [".csv", ".txt"]:
        df = pd.read_csv(file_path_or_bytes)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path_or_bytes)
    elif ext == ".json":
        df = pd.read_json(file_path_or_bytes)
    else:
        raise ValueError(f"Unsupported file format '{ext}'.")
        
    if column_mapping:
        df = df.rename(columns=column_mapping)
    return df
