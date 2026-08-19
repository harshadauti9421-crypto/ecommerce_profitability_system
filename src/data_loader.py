import os
import pandas as pd
import numpy as np
from utils.helpers import logger

CATEGORY_SUBCATEGORIES = {
    "Electronics": ["Smartphones", "Headphones", "Smartwatches", "Laptops", "Accessories"],
    "Fashion": ["Men's Apparel", "Women's Ethnic Wear", "Footwear", "Watches", "Handbags"],
    "Home & Kitchen": ["Cookware", "Home Decor", "Bedding", "Kitchen Appliances", "Storage"],
    "Beauty & Personal Care": ["Skincare", "Haircare", "Makeup", "Fragrances", "Grooming"],
    "Sports & Fitness": ["Gym Equipment", "Yoga Mats", "Sportswear", "Supplements", "Cycles"],
    "Toys & Games": ["Board Games", "Action Figures", "Educational Toys", "Puzzles", "Dolls"],
    "Books": ["Fiction", "Non-Fiction", "Competitive Exams", "Children Books", "Self-Help"],
    "Automotive": ["Car Accessories", "Helmets", "Riding Gear", "Cleaning Care", "Car Electronics"]
}

SEASONS = [
    "Diwali", "Holi", "Eid", "Christmas", "Navratri", 
    "Dussehra", "Raksha Bandhan", "Independence Day", "Republic Day", "Regular Season"
]

SEASON_MULTIPLIER = {
    "Diwali": 2.1,
    "Navratri": 1.7,
    "Dussehra": 1.6,
    "Holi": 1.5,
    "Eid": 1.5,
    "Christmas": 1.4,
    "Raksha Bandhan": 1.3,
    "Independence Day": 1.25,
    "Republic Day": 1.2,
    "Regular Season": 1.0
}

PLATFORMS = ["Amazon", "Flipkart", "Meesho", "Myntra", "Snapdeal"]
MARKETING_CHANNELS = ["Social Media", "Search Ads", "Influencer", "Email Marketing", "Organic Search", "Affiliate"]
COMPETITION_LEVELS = ["Low", "Medium", "High"]
REGIONS = ["North", "South", "West", "East", "Central"]

REGION_STATE_CITY = {
    "North": ("Delhi", "New Delhi"),
    "South": ("Karnataka", "Bengaluru"),
    "West": ("Maharashtra", "Mumbai"),
    "East": ("West Bengal", "Kolkata"),
    "Central": ("Rajasthan", "Jaipur")
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "COD", "Net Banking"]

REQUIRED_COLUMNS = [
    "product_category", "product_subcategory", "selling_price", "cost_price",
    "discount_percent", "advertising_cost", "shipping_cost", "return_rate",
    "product_rating", "season", "marketing_channel", "competition_level",
    "platform", "region", "state", "city", "payment_method", "demand", "revenue", "profit"
]

def generate_synthetic_data(num_records=43893, save_path=None, seed=42):
    """
    Generate realistic synthetic Indian e-commerce data with strong domain-specific relationships.
    """
    logger.info(f"Generating synthetic e-commerce dataset with {num_records} records (seed={seed})...")
    np.random.seed(seed)
    
    categories = np.random.choice(list(CATEGORY_SUBCATEGORIES.keys()), size=num_records)
    subcategories = []
    
    for cat in categories:
        subcats = CATEGORY_SUBCATEGORIES[cat]
        subcategories.append(np.random.choice(subcats))
        
    seasons = np.random.choice(SEASONS, size=num_records, p=[0.18, 0.08, 0.08, 0.08, 0.10, 0.08, 0.08, 0.06, 0.06, 0.20])
    platforms = np.random.choice(PLATFORMS, size=num_records, p=[0.35, 0.30, 0.15, 0.12, 0.08])
    channels = np.random.choice(MARKETING_CHANNELS, size=num_records)
    competition = np.random.choice(COMPETITION_LEVELS, size=num_records, p=[0.25, 0.50, 0.25])
    regions = np.random.choice(REGIONS, size=num_records)
    
    states = [REGION_STATE_CITY[r][0] for r in regions]
    cities = [REGION_STATE_CITY[r][1] for r in regions]
    payment_methods = np.random.choice(PAYMENT_METHODS, size=num_records, p=[0.50, 0.20, 0.10, 0.15, 0.05])
    
    # Generate numerical features tied to category
    selling_prices = []
    cost_prices = []
    return_rates = []
    
    for cat in categories:
        if cat == "Electronics":
            sp = np.random.uniform(1500, 25000)
            cost_ratio = np.random.uniform(0.65, 0.85)
            ret = np.random.uniform(3.0, 12.0)
        elif cat == "Fashion":
            sp = np.random.uniform(300, 4500)
            cost_ratio = np.random.uniform(0.35, 0.55)
            ret = np.random.uniform(12.0, 28.0) # Fashion has high returns
        elif cat == "Home & Kitchen":
            sp = np.random.uniform(500, 8000)
            cost_ratio = np.random.uniform(0.45, 0.65)
            ret = np.random.uniform(4.0, 14.0)
        elif cat == "Beauty & Personal Care":
            sp = np.random.uniform(200, 3000)
            cost_ratio = np.random.uniform(0.30, 0.50)
            ret = np.random.uniform(2.0, 8.0)
        elif cat == "Books":
            sp = np.random.uniform(150, 1500)
            cost_ratio = np.random.uniform(0.40, 0.60)
            ret = np.random.uniform(1.5, 6.0)
        else:
            sp = np.random.uniform(400, 6000)
            cost_ratio = np.random.uniform(0.40, 0.70)
            ret = np.random.uniform(3.0, 15.0)
            
        selling_prices.append(round(sp, 2))
        cost_prices.append(round(sp * cost_ratio, 2))
        return_rates.append(round(ret, 2))
        
    selling_prices = np.array(selling_prices)
    cost_prices = np.array(cost_prices)
    return_rates = np.array(return_rates)
    
    discount_percent = np.round(np.random.uniform(5.0, 55.0, size=num_records), 2)
    advertising_cost = np.round(np.random.uniform(500, 40000, size=num_records), 2)
    shipping_cost = np.round(np.random.uniform(40, 350, size=num_records), 2)
    product_rating = np.round(np.random.uniform(2.5, 4.9, size=num_records), 2)
    
    # Calculate realistic demand based on economic signals
    # Base demand: inversely related to selling price log, boosted by rating, discount, season, ad spend
    price_factor = 25000.0 / (selling_prices ** 0.5 + 50.0)
    rating_factor = (product_rating / 3.5) ** 1.8
    discount_factor = 1.0 + (discount_percent / 40.0)
    season_factor = np.array([SEASON_MULTIPLIER[s] for s in seasons])
    ad_factor = 1.0 + (advertising_cost / 15000.0) ** 0.45
    comp_factor = np.where(competition == "Low", 1.2, np.where(competition == "Medium", 1.0, 0.78))
    
    raw_demand = price_factor * rating_factor * discount_factor * season_factor * ad_factor * comp_factor
    # Add multiplicative noise (Gaussian around 1.0)
    noise = np.random.normal(1.0, 0.12, size=num_records)
    demand = np.clip(np.round(raw_demand * noise), 10, 15000).astype(int)
    
    # Calculate revenue & profit logically
    net_price = selling_prices * (1.0 - discount_percent / 100.0)
    revenue = np.round(net_price * demand, 2)
    
    # Costs: Cost of Goods Sold (COGS) + Shipping + Advertising + Return Losses (restocking/damage ~25% of cost)
    cogs = cost_prices * demand
    shipping_total = shipping_cost * demand
    return_loss = (return_rates / 100.0) * demand * (cost_prices * 0.25 + shipping_cost * 0.5)
    
    total_cost = cogs + shipping_total + advertising_cost + return_loss
    profit = np.round(revenue - total_cost, 2)
    
    descriptors = ["Premium", "Pro", "Ultra", "Smart", "Elite", "Classic", "Luxury", "Standard", "Advanced", "Digital"]
    product_names = [f"{np.random.choice(descriptors)} {subcat}" for subcat in subcategories]
    
    df = pd.DataFrame({
        "product_name": product_names,
        "product_category": categories,
        "product_subcategory": subcategories,
        "selling_price": selling_prices,
        "cost_price": cost_prices,
        "discount_percent": discount_percent,
        "advertising_cost": advertising_cost,
        "shipping_cost": shipping_cost,
        "return_rate": return_rates,
        "product_rating": product_rating,
        "season": seasons,
        "marketing_channel": channels,
        "competition_level": competition,
        "platform": platforms,
        "region": regions,
        "state": states,
        "city": cities,
        "payment_method": payment_methods,
        "demand": demand,
        "revenue": revenue,
        "profit": profit
    })
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        logger.info(f"Dataset successfully saved to {save_path}")
        
    return df

def get_product_name_col(df):
    """Detect product name column from dataset."""
    candidates = ["product_name", "Product Name", "product", "Product"]
    for c in candidates:
        if c in df.columns:
            return c
    return None

def load_and_validate_data(file_path):
    """
    Load data from file path or generate synthetic dataset if not found.
    Validates required columns and removes corrupted/NaN rows.
    """
    if not os.path.exists(file_path):
        logger.warning(f"File {file_path} not found. Generating default synthetic dataset...")
        df = generate_synthetic_data(num_records=43893, save_path=file_path)
    else:
        logger.info(f"Loading dataset from {file_path}...")
        df = pd.read_csv(file_path)
        
    prod_col = get_product_name_col(df)
    if not prod_col:
        descriptors = ["Premium", "Pro", "Ultra", "Smart", "Elite", "Classic", "Luxury", "Standard", "Advanced", "Digital"]
        df["product_name"] = [f"{descriptors[i % len(descriptors)]} {subcat}" for i, subcat in enumerate(df["product_subcategory"])]
        prod_col = "product_name"
        
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset missing required columns: {missing_cols}")
        
    # Drop NAs if any
    initial_len = len(df)
    df = df.dropna(subset=REQUIRED_COLUMNS).copy()
    if len(df) < initial_len:
        logger.info(f"Dropped {initial_len - len(df)} rows containing missing values.")
        
    logger.info(f"Dataset loaded and validated successfully. Total rows: {len(df)}")
    return df
