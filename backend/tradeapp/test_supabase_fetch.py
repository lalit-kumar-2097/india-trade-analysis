from supabase_client import supabase  
import pandas as pd

def fetch_data_for_forecast(hs_code: str):
    res = supabase.table("monthly_exports") \
        .select("*") \
        .eq("hs_code", hs_code) \
        .gte("month_curr", "2023-01-01") \
        .execute()
    return res.data

# Test it
if __name__ == "__main__":
    hs_code = "01069000"  # Example HS code
    print(f"Fetching data for HS code: {hs_code}")
    data = fetch_data_for_forecast(hs_code)
    df = pd.DataFrame(data)
    print(df.head())
