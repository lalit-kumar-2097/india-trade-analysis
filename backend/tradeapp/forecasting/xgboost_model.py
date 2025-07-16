
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def create_lag_features(df, lags=3):
    df = df.sort_values("ds")  # sort by 'ds', not 'month_curr'
    for i in range(1, lags + 1):
        df[f'lag_{i}'] = df['y'].shift(i)
    df.dropna(inplace=True)
    return df


def forecast_with_xgboost(df, validation=False):
    print("Incoming DF columns:", df.columns)
    df = df.copy()
    df = df[["month_curr", "value_curr"]].rename(columns={"month_curr": "ds", "value_curr": "y"})
    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = pd.to_numeric(df['y'], errors='coerce').fillna(0)

    df = create_lag_features(df, lags=3)

    if df.shape[0] < 6:
        raise ValueError("Not enough data to run validation.")

    features = [f'lag_{i}' for i in range(1, 4)]

    if validation:
        train = df.iloc[:-3]
        test = df.iloc[-3:]

        X_train = train[features]
        y_train = train['y']
        X_test = test[features]
        y_test = test['y']

        model = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)

        return {
            "mae": mae,
            "rmse": rmse,
            "actuals": y_test.tolist(),
            "predictions": y_pred.tolist()
        }

    # Normal forecasting (no validation)
    X = df[features]
    y = df['y']

    model = XGBRegressor(n_estimators=100, learning_rate=0.1)
    model.fit(X, y)

    last_known = df.iloc[-1][features].values
    current_date = df['ds'].max()
    future_preds = []

    for i in range(3):
        yhat = model.predict([last_known])[0]
        current_date += pd.DateOffset(months=1)
        future_preds.append({
            "ds": current_date.strftime("%Y-%m-%dT00:00:00"),
            "yhat": float(yhat),
            "yhat_lower": float(yhat * 0.8),
            "yhat_upper": float(yhat * 1.2)
        })
        last_known = np.roll(last_known, -1)
        last_known[-1] = yhat

    return pd.DataFrame(future_preds)
