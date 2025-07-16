# import pandas as pd
# import numpy as np
# from xgboost import XGBRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error

# def create_lag_features(df, lags=3):
#     df = df.sort_values("ds")  # sort by 'ds', not 'month_curr'
#     for i in range(1, lags + 1):
#         df[f'lag_{i}'] = df['y'].shift(i)
#     df.dropna(inplace=True)
#     return df

# def forecast_with_xgboost(df):
#     print("Incoming DF columns:", df.columns)
    
#     # Step 1: Preprocess
#     df = df.copy()
    
#     if 'month_curr' not in df.columns or 'value_curr' not in df.columns:
#         raise ValueError("Required columns 'month_curr' and/or 'value_curr' not found in input DataFrame.")

#     df = df[["month_curr", "value_curr"]].rename(columns={"month_curr": "ds", "value_curr": "y"})
#     df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
#     df['y'] = pd.to_numeric(df['y'], errors='coerce')

#     df.dropna(subset=['ds', 'y'], inplace=True)

#     # Step 2: Create lag features
#     df = create_lag_features(df, lags=3)

#     if df.empty:
#         raise ValueError("Not enough data after creating lag features.")

#     # Step 3: Train model
#     features = [f'lag_{i}' for i in range(1, 4)]
#     X = df[features]
#     y = df['y']

#     model = XGBRegressor(n_estimators=100, learning_rate=0.1)
#     model.fit(X, y)

#     # Step 4: Forecast next 3 months
#     last_known = df.iloc[-1][features].values
#     current_date = df['ds'].max()

#     future_preds = []
#     for i in range(3):
#         yhat = model.predict([last_known])[0]
#         current_date += pd.DateOffset(months=1)
#         future_preds.append({
#             "ds": current_date.strftime("%Y-%m-%dT00:00:00"),
#             "yhat": float(yhat),
#             "yhat_lower": float(yhat * 0.8),  # Simulated lower bound
#             "yhat_upper": float(yhat * 1.2)   # Simulated upper bound
#         })

#         # Update lag features for next forecast step
#         last_known = np.roll(last_known, -1)
#         last_known[-1] = yhat

#     return pd.DataFrame(future_preds)


# This function uses XGBoost to forecast the next 3 months based on lag features.
# It creates lag features from the last 3 months, trains the model, and predicts future values.
# The output is formatted similarly to Prophet's output with 'ds', 'yhat', 'yhat_lower', and 'yhat_upper'.
# The function handles missing values and ensures the input DataFrame has the required columns.
# It raises errors if the input DataFrame is empty or if required columns are missing.
# The forecasted values are returned in a DataFrame with the appropriate structure.
# The function also includes defensive checks to ensure the input data is valid for training the model.
# The model is trained using the last known values to predict future values for the next 3 months.
# The predicted values are returned in a DataFrame with the date, predicted value, and simulated confidence intervals.
# The function is designed to be robust against common data issues and provides clear error messages.
# It uses XGBoost's regression capabilities to handle the forecasting task efficiently.
# The function is suitable for time series forecasting tasks where historical data is available.
# The output DataFrame contains the forecasted dates and values, mimicking the structure of Prophet's output.
# The function is flexible and can be adapted for different lag periods or model parameters as needed.
# It is designed to be used in a larger forecasting pipeline where different models can be selected
# based on user preference or data characteristics.
# The function can be easily integrated into a Django application for real-time forecasting.
# The XGBoost model is configured with basic parameters, but can be tuned further for better performance.
# The function assumes the input DataFrame is pre-processed and contains the necessary columns for forecasting.
# It is expected to be called with a DataFrame that has monthly data for the 'month_curr' and 'value_curr' columns.
# The function is efficient and leverages XGBoost's capabilities to handle large datasets and complex relationships.
# The output is designed to be user-friendly
# 12 July 2025



from sklearn.metrics import mean_squared_error, mean_absolute_error
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
        rmse = mean_squared_error(y_test, y_pred, squared=False)

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
