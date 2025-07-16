# # from prophet import Prophet
# # import pandas as pd

# # def forecast_trade(df: pd.DataFrame, periods: int = 3):
# #     if df.empty:
# #         return pd.DataFrame()

# #     # Prepare the data
# #     data = df[['month_curr', 'value_curr']].copy()
# #     data = data.rename(columns={'month_curr': 'ds', 'value_curr': 'y'})

# #     # Prophet expects datetime + numeric
# #     data['ds'] = pd.to_datetime(data['ds'])
# #     data['y'] = pd.to_numeric(data['y'], errors='coerce').fillna(0)

# #     # Filter out rows with y=0 (optional)
# #     data = data[data['y'] > 0]
# #     if data.shape[0] < 2:
# #         return pd.DataFrame()  # Not enough data to forecast

# #     # Train model
# #     model = Prophet()
# #     model.fit(data)

# #     # Forecast next N months
# #     future = model.make_future_dataframe(periods=periods, freq='M')
# #     forecast = model.predict(future)

# #     result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
# #     result['yhat'] = result['yhat'].round(2)
# #     result['yhat_lower'] = result['yhat_lower'].round(2)
# #     result['yhat_upper'] = result['yhat_upper'].round(2)
    
# #     return result


# from prophet import Prophet
# import pandas as pd

# def forecast_with_prophet(df, periods=3):
#     df = df[['month_curr', 'value_curr']].copy()
#     df.rename(columns={'month_curr': 'ds', 'value_curr': 'y'}, inplace=True)
#     df['ds'] = pd.to_datetime(df['ds'])
#     df['y'] = pd.to_numeric(df['y'])

#     model = Prophet()
#     model.fit(df)

#     future = model.make_future_dataframe(periods=periods, freq='M')
#     forecast = model.predict(future)

#     return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)


from prophet import Prophet
import pandas as pd


def forecast_with_prophet(df, validation=False):
    from prophet import Prophet
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    if len(df) < 3:
        raise ValueError("Not enough data to forecast. At least 3 months of data is required.")

    df = df.copy()
    df = df[["month_curr", "value_curr"]].rename(columns={"month_curr": "ds", "value_curr": "y"})
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"], errors="coerce").fillna(0)

    # Sort by date
    df = df.sort_values("ds")

    if validation:
        train_df = df.iloc[:-3]  # All except last 3
        test_df = df.iloc[-3:]   # Last 3 months
    else:
        train_df = df

    model = Prophet()
    model.fit(train_df)

    future = model.make_future_dataframe(periods=3, freq='MS')
    forecast = model.predict(future)

    # Only take future predictions (last 3 rows)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(3)

    if validation:
        y_true = test_df['y'].values
        y_pred = result['yhat'].values
        mae = mean_absolute_error(y_true, y_pred)
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        return {
            "mae": float(mae),
            "rmse": float(rmse),
            "actuals": y_true.tolist(),
            "predictions": y_pred.tolist(),
        }

    return result
