# # # This view handles the forecasting request.
# # # It expects a POST request with JSON data containing 'hs_code', 'model', and optionally 'validation'.
# # # It fetches the relevant data from Supabase, processes it, and returns the forecasted data.
# # # If no data is found for the given HS code, it returns a 404 error.
# # # If the data is insufficient for forecasting, it returns a 400 error with a specific message.
# # # If an unexpected error occurs, it returns a 500 error with the error message.
# # # If the request is successful, it returns the forecasted data in JSON format.



# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import HttpResponse
# from ..supabase_client import supabase
# from ..forecasting.model_selector import run_forecast
# from ..utils.log_utils import log_forecast
# import pandas as pd

# @api_view(['POST'])
# def forecast_view(request):
#     # Input
#     hs_code = request.data.get("hs_code")
#     model_name = request.data.get("model", "prophet")

#     # ✅ Convert validation_mode to bool if passed as string
#     validation_mode = request.data.get("validation", False)
#     if isinstance(validation_mode, str):
#         validation_mode = validation_mode.lower() == "true"
#     # validation_mode = request.data.get("validation", False)

#     # Django session for logging
#     session_id = request.session.session_key
#     if not session_id:
#         request.session.create()
#         session_id = request.session.session_key

#     # Fetch from Supabase
#     response = supabase.table("monthly_exports").select("*").eq("hs_code", hs_code).execute()
#     df = pd.DataFrame(response.data)
#     print('Data fetched from Supabase: Delete this line from forecast_views.py') # Debugging line to check data fetched Remove it later
#     print(df.columns, df.head())

#     if df.empty:
#         log_forecast(
#             hs_code, model_name, validation_mode,
#             status="no_data",
#             message="No data found for HS code.",
#             session_id=session_id
#         )
#         return Response({"error": "No data found for the given HS code."}, status=404)    

#     # Forecasting
#     try:
#         forecast = run_forecast(df, model=model_name, validation=validation_mode)
#     except ValueError as e:
#         log_forecast(
#             hs_code, model_name, validation_mode,
#             status="error",
#             message=str(e),
#             session_id=session_id
#         )
#         print('there was an error in the forecast', e)
#         return Response({"error": str(e)}, status=400)
#     except Exception as e:
#         log_forecast(hs_code, model_name, validation_mode, status="error", message=str(e), session_id=session_id)
#         print('there was an unexpected error in the forecast in except', e)
#         return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

#     # Log & Return
#     if isinstance(forecast, dict) and "mae" in forecast:
#         log_forecast(
#             hs_code, model_name, validation_mode, status="success",
#             message="Validation run",
#             mae=forecast["mae"], rmse=forecast["rmse"],
#             session_id=session_id
#         )
#         return Response(forecast)

#     log_forecast(
#         hs_code, model_name, validation_mode, status="success",
#         message="Forecast successful",
#         session_id=session_id
#     )
#     return Response(forecast.to_dict(orient="records"))



# 16 July 2025

from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..supabase_client import supabase
from ..forecasting.model_selector import run_forecast
from ..utils.log_utils import log_forecast
import pandas as pd

@api_view(['POST'])
def forecast_view(request):
    # Input parameters
    hs_code = request.data.get("hs_code")
    model_name = request.data.get("model", "prophet")

    # Convert validation_mode to boolean
    validation_mode = request.data.get("validation", False)
    if isinstance(validation_mode, str):
        validation_mode = validation_mode.lower() == "true"

    # Django session for logging
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Fetch data from Supabase
    response = supabase.table("monthly_exports").select("*").eq("hs_code", hs_code).execute()
    df = pd.DataFrame(response.data)

    if df.empty:
        log_forecast(
            hs_code, model_name, validation_mode,
            status="no_data",
            message="No data found for HS code.",
            session_id=session_id
        )
        return Response({"error": "No data found for the given HS code."}, status=404)

    # Extract commodity name (assumes it's consistent for all rows)
    commodity_name = df.iloc[0].get('commodity', 'commodity')

    # Forecasting
    try:
        forecast = run_forecast(df, model=model_name, validation=validation_mode)
    except ValueError as e:
        log_forecast(
            hs_code, model_name, validation_mode,
            status="error",
            message=str(e),
            session_id=session_id
        )
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        log_forecast(
            hs_code, model_name, validation_mode,
            status="error",
            message=str(e),
            session_id=session_id
        )
        return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

    # Prepare Response
    if isinstance(forecast, dict) and "mae" in forecast:
        # Validation mode
        log_forecast(
            hs_code, model_name, validation_mode,
            status="success",
            message="Validation run",
            mae=forecast["mae"],
            rmse=forecast["rmse"],
            session_id=session_id
        )
        return Response({
            "commodity_name": commodity_name,
            "predictions": forecast["predictions"],
            "actuals": forecast["actuals"],
            "mae": forecast["mae"],
            "rmse": forecast["rmse"]
        })

    # Normal forecast mode
    log_forecast(
        hs_code, model_name, validation_mode,
        status="success",
        message="Forecast successful",
        session_id=session_id
    )
    return Response({
        "commodity_name": commodity_name,
        "forecast": forecast.to_dict(orient="records")
    })


# This code handles the forecasting request, fetching data from Supabase, processing it, and returning the forecasted data.
# If no data is found for the given HS code, it returns a 404 error.
# If the data is insufficient for forecasting, it returns a 400 error with a specific message.
# If an unexpected error occurs, it returns a 500 error with the error message. 