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
    """
    df = df.copy()
    
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
