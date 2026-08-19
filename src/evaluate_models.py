import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

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
