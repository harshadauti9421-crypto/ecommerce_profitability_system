import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def calculate_metrics(y_true, y_pred):
    """
    Calculate dynamic performance metrics: R2, MAE, RMSE, MAPE.
    Zero hardcoding. Guaranteed clean numerical outputs with zero-division handling.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    r2 = float(r2_score(y_true, y_pred))
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    
    # Safe MAPE calculation handling zeros in y_true
    non_zero_mask = y_true != 0
    if np.any(non_zero_mask):
        mape = float(np.mean(np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask])) * 100.0)
    else:
        mape = 0.0
        
    return {
        "R2": round(r2, 4),
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2)
    }

def _extract_metric_val(model_dict, keys_to_check):
    """Safely extract float metric from flat or nested dict with key variations."""
    if not isinstance(model_dict, dict):
        return None
    
    # Direct search
    for k in keys_to_check:
        if k in model_dict and model_dict[k] is not None:
            try:
                val = float(model_dict[k])
                if not np.isnan(val):
                    return val
            except (ValueError, TypeError):
                pass

    # Nested search in "test" or "val"
    for sub in ["test", "val"]:
        if sub in model_dict and isinstance(model_dict[sub], dict):
            for k in keys_to_check:
                if k in model_dict[sub] and model_dict[sub][k] is not None:
                    try:
                        val = float(model_dict[sub][k])
                        if not np.isnan(val):
                            return val
                    except (ValueError, TypeError):
                        pass

    return None

def extract_model_evaluation_record(name, model_info):
    """
    Extract normalized evaluation record containing test_rmse, test_mae, test_r2, val_r2, overfitting_gap.
    Returns None if the model is failed, skipped, or missing essential test metrics.
    """
    if not isinstance(model_info, dict):
        return None

    # Exclude failed/skipped models
    status = model_info.get("Status") or model_info.get("status")
    if status and str(status).lower() in ["failed", "skipped", "unavailable"]:
        return None

    test_rmse = _extract_metric_val(model_info, ["RMSE (₹)", "Test RMSE", "RMSE", "Test_RMSE", "test_rmse", "rmse"])
    test_mae  = _extract_metric_val(model_info, ["MAE (₹)", "Test MAE", "MAE", "Test_MAE", "test_mae", "mae"])
    test_r2   = _extract_metric_val(model_info, ["Test R²", "Test R2", "test_r2", "Test_R2", "R2", "r2"])
    val_r2    = _extract_metric_val(model_info, ["Validation R²", "Val R2", "Validation_R2", "val_r2", "val_R2"])

    # If test_r2 not found under direct search, check nested test dict specifically
    if test_r2 is None and "test" in model_info and isinstance(model_info["test"], dict):
        test_r2 = _extract_metric_val(model_info["test"], ["R2", "r2"])
    if val_r2 is None and "val" in model_info and isinstance(model_info["val"], dict):
        val_r2 = _extract_metric_val(model_info["val"], ["R2", "r2"])

    if test_rmse is None or test_mae is None or test_r2 is None:
        return None

    if val_r2 is None:
        val_r2 = test_r2

    # Overfitting Gap = Validation R² - Test R²
    overfitting_gap = _extract_metric_val(model_info, ["Overfitting Gap", "overfitting_gap"])
    if overfitting_gap is None:
        overfitting_gap = round(val_r2 - test_r2, 4)

    return {
        "model_name": name,
        "test_rmse": round(test_rmse, 4),
        "test_mae": round(test_mae, 4),
        "test_r2": round(test_r2, 4),
        "val_r2": round(val_r2, 4),
        "overfitting_gap": round(overfitting_gap, 4),
        "raw_info": model_info
    }

def rank_and_select_models(models_dict, tolerance=1e-5):
    """
    Ranks evaluated models using the exact 4-tier lexicographic decision hierarchy:
    1. Primary: Lowest Test RMSE (ascending)
    2. Secondary: Lowest Test MAE (ascending)
    3. Tertiary: Highest Test R² (descending)
    4. Quaternary: Lowest Overfitting Gap (ascending)

    Returns:
        tuple: (best_model_name, selection_reason, ranked_records_list)
        If no valid models: (None, "No valid model available for selection. Please check model training and evaluation results.", [])
    """
    if not models_dict or not isinstance(models_dict, dict):
        return None, "No valid model available for selection. Please check model training and evaluation results.", []

    valid_records = []
    for name, info in models_dict.items():
        rec = extract_model_evaluation_record(name, info)
        if rec is not None:
            valid_records.append(rec)

    if not valid_records:
        return None, "No valid model available for selection. Please check model training and evaluation results.", []

    # Sort lexicographically according to hierarchy
    valid_records.sort(key=lambda r: (r["test_rmse"], r["test_mae"], -r["test_r2"], r["overfitting_gap"]))

    winner = valid_records[0]

    if len(valid_records) == 1:
        reason = f"Selected '{winner['model_name']}' as the sole validly evaluated model."
    else:
        runner_up = valid_records[1]
        rmse_diff = abs(winner["test_rmse"] - runner_up["test_rmse"])
        mae_diff = abs(winner["test_mae"] - runner_up["test_mae"])
        r2_diff = abs(winner["test_r2"] - runner_up["test_r2"])

        if rmse_diff > tolerance:
            reason = f"Selected because it achieved the lowest Test RMSE ({winner['test_rmse']:.2f} vs runner-up '{runner_up['model_name']}' {runner_up['test_rmse']:.2f})."
        elif mae_diff > tolerance:
            reason = f"Selected because Test RMSE was tied ({winner['test_rmse']:.2f}) and it achieved the lowest Test MAE ({winner['test_mae']:.2f} vs '{runner_up['model_name']}' {runner_up['test_mae']:.2f})."
        elif r2_diff > tolerance:
            reason = f"Selected because Test RMSE and Test MAE were tied and it achieved the highest Test R² ({winner['test_r2']:.4f} vs '{runner_up['model_name']}' {runner_up['test_r2']:.4f})."
        else:
            reason = f"Selected because primary metrics were tied and it achieved the lowest Overfitting Gap ({winner['overfitting_gap']:.4f} vs '{runner_up['model_name']}' {runner_up['overfitting_gap']:.4f})."

    return winner["model_name"], reason, valid_records

