
from sklearn.metrics import root_mean_squared_error
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
        rmse = root_mean_squared_error(y_true, y_pred)

        # rmse = mean_squared_error(y_true, y_pred, squared=False)
        return {
            "mae": float(mae),
            "rmse": float(rmse),
            "actuals": y_true.tolist(),
            "predictions": y_pred.tolist(),
        }

    return result
