import json
import os

metrics_path = os.path.join("models", "model_metrics.json")
if os.path.exists(metrics_path):
    with open(metrics_path, "r") as f:
        d = json.load(f)
    print("BEST DEMAND MODEL:", d["demand"]["best_model"])
    print("BEST PROFIT MODEL:", d["profit"]["best_model"])
    for tgt in ["demand", "profit"]:
        print(f"\n=== {tgt.upper()} METRICS ===")
        for m, vals in d[tgt]["models"].items():
            t = vals["test"]
            print(f"{m:26s} | R2: {t['R2']:6.4f} | MAE: {t['MAE']:8.2f} | RMSE: {t['RMSE']:8.2f} | MAPE: {t['MAPE']}%")
else:
    print("Metrics file not created yet.")
