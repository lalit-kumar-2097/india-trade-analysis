from .prophet_model import forecast_with_prophet
from .sarima_model import forecast_with_sarima
from .xgboost_model import forecast_with_xgboost


def run_forecast(df, model="prophet", validation=False):
    if model == "sarima":
        return forecast_with_sarima(df, validation=validation)
    elif model == "xgboost":
        return forecast_with_xgboost(df, validation=validation)
    return forecast_with_prophet(df, validation=validation)

# This function selects the forecasting model based on the input parameter.
# It supports Prophet, SARIMA, and XGBoost models.
# If no model is specified, it defaults to Prophet.
# The function takes a DataFrame `df` and a string `model` as inputs.
# It returns the forecasted DataFrame based on the selected model.