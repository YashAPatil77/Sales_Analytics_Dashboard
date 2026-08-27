"""
Forecasting Module for Sales Analytics Dashboard.

Provides monthly sales time-series aggregation, trend/seasonality decomposition,
Holt-Winters Exponential Smoothing forecasting, confidence bounds, and error evaluation metrics.
Includes resilient fallback forecasting for environments missing statsmodels/scikit-learn.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

# Resilient Imports with Zero-Crash Fallbacks
try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    HAS_STATSMODELS = True
except (ImportError, ModuleNotFoundError):
    HAS_STATSMODELS = False

try:
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    HAS_SKLEARN = True
except (ImportError, ModuleNotFoundError):
    HAS_SKLEARN = False

def _calc_mae(y_true, y_pred) -> float:
    if HAS_SKLEARN:
        return float(mean_absolute_error(y_true, y_pred))
    return float(np.mean(np.abs(y_true - y_pred)))

def _calc_rmse(y_true, y_pred) -> float:
    if HAS_SKLEARN:
        return float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

def prepare_monthly_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates order data into a clean monthly time series (Month Start frequency).
    """
    data = df.copy()
    if 'Order Date' not in data.columns or not pd.api.types.is_datetime64_any_dtype(data['Order Date']):
        data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
        
    monthly = data.set_index('Order Date').resample('MS').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Quantity=('Quantity', 'sum')
    ).reset_index()

    return monthly.sort_values(by='Order Date')

def train_sales_forecast(monthly_df: pd.DataFrame, forecast_periods: int = 6) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Trains Exponential Smoothing (Holt-Winters) model on monthly sales data
    and generates multi-month out-of-sample forecast with confidence bounds.
    Falls back gracefully to trend regression if statsmodels is unavailable.
    """
    if not HAS_STATSMODELS or len(monthly_df) < 12:
        return _fallback_linear_forecast(monthly_df, forecast_periods)

    ts_data = monthly_df.set_index('Order Date')['Sales']
    
    # Fit Holt-Winters model with additive trend & seasonal periods
    try:
        model = ExponentialSmoothing(
            ts_data,
            trend='add',
            seasonal='add',
            seasonal_periods=12,
            initialization_method="estimated"
        ).fit()
    except Exception:
        try:
            model = ExponentialSmoothing(
                ts_data,
                trend='add',
                initialization_method="estimated"
            ).fit()
        except Exception:
            return _fallback_linear_forecast(monthly_df, forecast_periods)

    fitted_values = model.fittedvalues
    
    # Calculate error metrics on in-sample fit
    mae = _calc_mae(ts_data, fitted_values)
    rmse = _calc_rmse(ts_data, fitted_values)
    mape = float(np.mean(np.abs((ts_data - fitted_values) / np.maximum(1, ts_data))) * 100.0)

    metrics = {
        'MAE': float(mae),
        'RMSE': float(rmse),
        'MAPE': float(mape)
    }

    # Generate future forecast dates
    last_date = ts_data.index[-1]
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
    
    forecast_values = model.forecast(forecast_periods)
    forecast_values = np.clip(forecast_values, a_min=0, a_max=None)

    residuals = ts_data - fitted_values
    std_residual = np.std(residuals)

    hist_df = pd.DataFrame({
        'Date': ts_data.index,
        'Sales': ts_data.values,
        'Type': 'Actual Historical',
        'Lower Bound': ts_data.values,
        'Upper Bound': ts_data.values
    })

    z = 1.96
    lower_bound = np.clip(forecast_values - (z * std_residual), a_min=0, a_max=None)
    upper_bound = forecast_values + (z * std_residual)

    fc_df = pd.DataFrame({
        'Date': future_dates,
        'Sales': forecast_values,
        'Type': 'Forecast',
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound
    })

    combined_df = pd.concat([hist_df, fc_df], ignore_index=True)
    return combined_df, metrics

def _fallback_linear_forecast(monthly_df: pd.DataFrame, forecast_periods: int = 6) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Fallback trend forecasting using Polynomial / Moving Average trend.
    """
    ts_data = monthly_df.set_index('Order Date')['Sales']
    X = np.arange(len(ts_data)).reshape(-1, 1)
    y = ts_data.values

    slope, intercept = np.polyfit(X.flatten(), y, 1)
    fitted = slope * X.flatten() + intercept

    mae = _calc_mae(y, fitted)
    rmse = _calc_rmse(y, fitted)
    mape = float(np.mean(np.abs((y - fitted) / np.maximum(1, y))) * 100.0)

    last_date = ts_data.index[-1]
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
    future_X = np.arange(len(ts_data), len(ts_data) + forecast_periods)
    future_y = np.clip(slope * future_X + intercept, a_min=0, a_max=None)

    std_res = np.std(y - fitted)

    hist_df = pd.DataFrame({
        'Date': ts_data.index,
        'Sales': ts_data.values,
        'Type': 'Actual Historical',
        'Lower Bound': ts_data.values,
        'Upper Bound': ts_data.values
    })

    fc_df = pd.DataFrame({
        'Date': future_dates,
        'Sales': future_y,
        'Type': 'Forecast',
        'Lower Bound': np.clip(future_y - 1.96 * std_res, a_min=0, a_max=None),
        'Upper Bound': future_y + 1.96 * std_res
    })

    return pd.concat([hist_df, fc_df], ignore_index=True), {'MAE': float(mae), 'RMSE': float(rmse), 'MAPE': float(mape)}
