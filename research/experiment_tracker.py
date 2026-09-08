import os
import json
import pandas as pd
from datetime import datetime
from utils.helpers import logger

RESULTS_DIR = "research_results"

def initialize_research_dir():
    """Ensure research_results directory and subfolders exist."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "figures"), exist_ok=True)

def log_experiment_run(experiment_id, dataset_name, dataset_type, metrics, hypothesis_results=None, seed=42):
    """
    Log an experimental run metadata to research_results/experiment_log.json
    """
    initialize_research_dir()
    log_path = os.path.join(RESULTS_DIR, "experiment_log.json")
    
    entry = {
        "experiment_id": experiment_id,
        "timestamp": datetime.now().isoformat(),
        "dataset_name": dataset_name,
        "dataset_type": dataset_type,
        "random_seed": seed,
        "metrics": metrics,
        "hypothesis_results": hypothesis_results or {}
    }
    
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
            
    logs.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
        
    logger.info(f"Logged research experiment '{experiment_id}' to {log_path}")
    return entry
