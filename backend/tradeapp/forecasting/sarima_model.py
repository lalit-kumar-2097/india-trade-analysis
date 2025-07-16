from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import numpy as np
import pandas as pd
import statsmodels.api as sm

def forecast_with_sarima(df, validation=False):
    df = df.copy()    
    df = df[["month_curr", "value_curr"]].rename(columns={"month_curr": "ds", "value_curr": "y"})
    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = pd.to_numeric(df['y'], errors='coerce').fillna(0)
    if df.shape[0] < 12 or df['y'].sum() == 0:
        raise ValueError("Not enough data points or all-zero values to train SARIMA.")

    if validation:
        train_df = df.iloc[:-3]
        test_df = df.iloc[-3:]

        model = sm.tsa.SARIMAX(train_df['y'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        results = model.fit(disp=False)
        forecast = results.forecast(steps=3)

        predictions = forecast.tolist()
        actuals = test_df['y'].tolist()

        mae = mean_absolute_error(actuals, predictions)
        rmse = root_mean_squared_error(actuals, predictions)

        return {
            "mae": mae,
            "rmse": rmse,
            "actuals": actuals,
            "predictions": predictions
        }

    # regular forecasting code...
    model = sm.tsa.SARIMAX(df['y'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit(disp=False)
    forecast = results.forecast(steps=3)

    current_date = df['ds'].max()
    predictions = []

    for val in forecast:
        current_date += pd.DateOffset(months=1)
        predictions.append({
            "ds": current_date.strftime("%Y-%m-%dT00:00:00"),
            "yhat": float(val),
            "yhat_lower": float(val * 0.8),
            "yhat_upper": float(val * 1.2)
        })

    return pd.DataFrame(predictions)
