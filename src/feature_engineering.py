import pandas as pd
import numpy as np

NUMERICAL_FEATURES = [
    "selling_price", "cost_price", "discount_percent", "advertising_cost",
    "shipping_cost", "return_rate", "product_rating", "net_price", "markup_ratio"
]

CATEGORICAL_FEATURES = [
    "product_category", "product_subcategory", "season", "marketing_channel",
    "competition_level", "platform", "region", "payment_method"
]

ALL_INPUT_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

def add_engineered_features(df):
    """
    Add domain-specific engineered features to the input DataFrame.
    Guarantees all NUMERICAL_FEATURES and CATEGORICAL_FEATURES exist with valid defaults.
    """
    df = df.copy()
    
    # Ensure numerical features exist
    num_defaults = {
        "selling_price": 0.0,
        "cost_price": 0.0,
        "discount_percent": 0.0,
        "advertising_cost": 0.0,
        "shipping_cost": 0.0,
        "return_rate": 0.05,
        "product_rating": 4.2
    }
    for col, default_val in num_defaults.items():
        if col not in df.columns:
            df[col] = default_val
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(default_val)
            
    # Ensure categorical features exist
    cat_defaults = {
        "product_category": "Technology",
        "product_subcategory": "Accessories",
        "season": "Regular Season",
        "marketing_channel": "Organic",
        "competition_level": "Medium",
        "platform": "Amazon",
        "region": "Central",
        "payment_method": "Credit Card"
    }
    for col, default_val in cat_defaults.items():
        if col not in df.columns:
            df[col] = default_val
        else:
            df[col] = df[col].fillna(default_val).astype(str)
            
    # Net unit selling price after discount
    df["net_price"] = np.round(df["selling_price"] * (1.0 - df["discount_percent"] / 100.0), 2)
    
    # Markup ratio (selling price vs cost price, with zero division protection)
    cost = np.where(df["cost_price"] <= 0, 0.01, df["cost_price"])
    df["markup_ratio"] = np.round(df["selling_price"] / cost, 4)
    
    return df

def prepare_feature_matrices(df, target_col):
    """
    Apply feature engineering and separate features X from target y.
    Guarantees no target leakage!
    """
    df_engineered = add_engineered_features(df)
    
    X = df_engineered[ALL_INPUT_FEATURES].copy()
    y = df_engineered[target_col].copy()
    
    return X, y
