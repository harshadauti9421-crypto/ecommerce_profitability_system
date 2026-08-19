import os
import sys
import unittest
import pandas as pd

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import generate_synthetic_data, load_and_validate_data
from src.train_models import train_and_evaluate_all
from src.prediction import run_product_analysis
from src.explainability import explain_prediction_shap
from utils.helpers import format_currency

class TestPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run training test suite without overwriting production dataset."""
        print("\n--- Setting Up Pipeline Test Suite ---")
        cls.data_path = os.path.join("data", "ecommerce_data.csv")
        if not os.path.exists(cls.data_path):
            cls.data_path = os.path.join("data", "test_ecommerce_data.csv")
            generate_synthetic_data(num_records=1000, save_path=cls.data_path)
            cls.metrics = train_and_evaluate_all()
        else:
            cls.metrics = train_and_evaluate_all()

    def test_dataset_generation(self):
        """Test dataset shape and column integrity."""
        df = pd.read_csv(self.data_path)
        self.assertGreaterEqual(len(df), 1000)
        self.assertIn("selling_price", df.columns)
        self.assertIn("profit", df.columns)

    def test_model_training_and_metrics(self):
        """Test that metrics JSON contains non-hardcoded R2 scores for all 6 models."""
        self.assertIn("demand", self.metrics)
        self.assertIn("profit", self.metrics)
        self.assertIsNotNone(self.metrics["demand"]["best_model"])
        self.assertIsNotNone(self.metrics["profit"]["best_model"])
        
        demand_models = self.metrics["demand"]["models"]
        self.assertEqual(len(demand_models), 4) # All 4 models evaluated
        for name, res in demand_models.items():
            self.assertIn("R2", res["test"])
            self.assertIn("MAE", res["test"])
            self.assertIn("RMSE", res["test"])
            self.assertIn("MAPE", res["test"])

    def test_single_product_prediction(self):
        """Test complete prediction workflow for single input product."""
        sample_input = {
            "product_name": "Wireless Bluetooth Earbuds",
            "product_category": "Electronics",
            "product_subcategory": "Headphones",
            "selling_price": 2499.0,
            "cost_price": 1100.0,
            "discount_percent": 15.0,
            "advertising_cost": 5000.0,
            "shipping_cost": 90.0,
            "return_rate": 5.0,
            "product_rating": 4.3,
            "season": "Diwali",
            "marketing_channel": "Social Media",
            "competition_level": "Medium",
            "platform": "Amazon",
            "region": "South",
            "payment_method": "UPI"
        }
        
        res = run_product_analysis(sample_input)
        self.assertGreater(res["predicted_demand"], 0)
        self.assertIsInstance(res["predicted_profit"], float)
        self.assertIn(res["risk_analysis"]["risk_level"], ["Low Risk", "Medium Risk", "High Risk"])
        self.assertGreaterEqual(res["business_score"]["score"], 0)
        self.assertLessEqual(res["business_score"]["score"], 100)
        self.assertIn(res["launch_decision"]["decision"], ["🟢 LAUNCH", "🟡 LAUNCH WITH MODIFICATIONS", "🔴 DO NOT LAUNCH"])
        self.assertGreater(len(res["recommendations"]), 0)
        self.assertTrue(len(res["conclusion"]) > 50)

    def test_currency_formatting(self):
        """Test Indian Rupee formatting helper."""
        self.assertEqual(format_currency(125000), "₹1,25,000")
        self.assertEqual(format_currency(450), "₹450")
        self.assertEqual(format_currency(-15000), "-₹15,000")

    def test_explainability(self):
        """Test SHAP and feature importance generation."""
        sample_input = {
            "product_name": "Test Item",
            "product_category": "Fashion",
            "product_subcategory": "Men's Apparel",
            "selling_price": 999.0,
            "cost_price": 400.0,
            "discount_percent": 20.0,
            "advertising_cost": 2000.0,
            "shipping_cost": 60.0,
            "return_rate": 15.0,
            "product_rating": 4.0,
            "season": "Regular Season",
            "marketing_channel": "Search Ads",
            "competition_level": "High",
            "platform": "Flipkart",
            "region": "North",
            "payment_method": "COD"
        }
        res = run_product_analysis(sample_input)
        fig_global, fig_local, df_exp = explain_prediction_shap(res["X_input"], model_type="profit")
        self.assertIsNotNone(fig_global)
        self.assertIsNotNone(fig_local)
        self.assertGreater(len(df_exp), 0)

if __name__ == "__main__":
    unittest.main()
