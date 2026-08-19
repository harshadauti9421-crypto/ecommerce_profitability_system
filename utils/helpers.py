import os
import json
import logging
from datetime import datetime

def setup_logger(name="ecommerce_system"):
    """Set up and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # File handler
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(os.path.join(log_dir, "system.log"), encoding="utf-8")
        fh.setLevel(logging.INFO)
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger

logger = setup_logger()

def format_currency(value):
    """Format numbers into Indian Rupee format (e.g. ₹1,25,000)."""
    try:
        val = float(value)
        is_negative = val < 0
        val = abs(val)
        
        # Convert to string integer representation
        s = f"{val:.0f}"
        if len(s) <= 3:
            res = s
        else:
            # Indian numbering format: 3 digits from right, then groups of 2
            last3 = s[-3:]
            other = s[:-3]
            groups = []
            while len(other) > 2:
                groups.insert(0, other[-2:])
                other = other[:-2]
            if other:
                groups.insert(0, other)
            res = ",".join(groups) + "," + last3
            
        sign = "-" if is_negative else ""
        return f"{sign}₹{res}"
    except Exception as e:
        logger.error(f"Error formatting currency value {value}: {str(e)}")
        return f"₹{value}"

def save_prediction_to_history(record, history_file_path):
    """Save analysis record into local JSON history file."""
    try:
        os.makedirs(os.path.dirname(history_file_path), exist_ok=True)
        history = []
        if os.path.exists(history_file_path):
            with open(history_file_path, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        
        # Add timestamp
        record_copy = dict(record)
        record_copy["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.insert(0, record_copy) # newest first
        
        # Keep maximum 100 entries
        history = history[:100]
        
        with open(history_file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved prediction record for '{record.get('product_name', 'Unknown')}' to history.")
        return True
    except Exception as e:
        logger.error(f"Failed to save prediction history: {str(e)}")
        return False

def load_prediction_history(history_file_path):
    """Load prediction history records from JSON file."""
    try:
        if os.path.exists(history_file_path):
            with open(history_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Failed to load prediction history: {str(e)}")
        return []
