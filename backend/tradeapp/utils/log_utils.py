from ..supabase_client import supabase


def log_forecast(hs_code, model, validation, status, message="", mae=None, rmse=None, session_id=None, user_id=None):
    log_data = {        
        "hs_code": hs_code,
        "model": model,
        "validation": validation,
        "status": status,
        "message": message,
        "mae": mae,
        "rmse": rmse,
        "session_id": session_id,  # Placeholder for session ID if needed
        "user_id": user_id,  # Placeholder for user ID if needed
    }
    try:
        supabase.table("forecast_logs").insert(log_data).execute()
        print("Forecast logged successfully:", log_data)        
    except Exception as e:
        print("Failed to log forecast:", e)
