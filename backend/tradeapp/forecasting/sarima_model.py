# import pandas as pd
# from pmdarima import auto_arima
# from statsmodels.tsa.statespace.sarimax import SARIMAX

# def forecast_with_sarima(df, periods=3):
#     # Prepare data
#     df = df[['month_curr', 'value_curr']].copy()
#     df.rename(columns={'month_curr': 'ds', 'value_curr': 'y'}, inplace=True)
#     df['ds'] = pd.to_datetime(df['ds'])
#     df = df.sort_values('ds')
#     df.set_index('ds', inplace=True)
#     df['y']= pd.to_numeric(df['y'], errors='coerce').fillna(0)
    
#     # ✅ Defensive check
#     if df.shape[0] < 12 or df['y'].sum() == 0:
#         raise ValueError("Not enough data points or all-zero values to train SARIMA.")

#     # Fit model using auto_arima to select best (p,d,q)(P,D,Q)s
#     stepwise_model = auto_arima(
#         df['y'],
#         seasonal=True,
#         m=12,  # monthly data
#         trace=False,
#         suppress_warnings=True,
#         error_action='ignore'
#     )

#     # Fit final SARIMAX model
#     model = SARIMAX(df['y'], order=stepwise_model.order, seasonal_order=stepwise_model.seasonal_order)
#     model_fit = model.fit(disp=False)

#     # Forecast next N months
#     forecast = model_fit.get_forecast(steps=periods)
#     forecast_index = pd.date_range(start=df.index[-1] + pd.offsets.MonthBegin(), periods=periods, freq='M')
#     pred = forecast.predicted_mean
#     conf_int = forecast.conf_int()

#     # Format output like Prophet
#     result = pd.DataFrame({
#         "ds": forecast_index,
#         "yhat": pred.values,
#         "yhat_lower": conf_int.iloc[:, 0].values,
#         "yhat_upper": conf_int.iloc[:, 1].values
#     })

#     return result
# 12 July 2025


from sklearn.metrics import mean_squared_error, mean_absolute_error
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
        rmse = mean_squared_error(actuals, predictions, squared=False)

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
