# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from ..supabase_client import supabase
# import pandas as pd

# @api_view(['GET'])
# def export_data_view(request):
#     hs_code = request.GET.get("hs_code")
#     limit = int(request.GET.get("limit", 12))
#     sort_order = request.GET.get("sort", "asc").lower()
#     year = request.GET.get("year")
#     month_from = request.GET.get("month_from")
#     month_to = request.GET.get("month_to")

#     if not hs_code:
#         return Response({"error": "hs_code is required"}, status=400)

#     # Base query
#     query = supabase.table("monthly_exports").select("*").eq("hs_code", hs_code)

#     if year:
#         query = query.ilike("month_curr", f"{year}-%")
    
#     # Sorting
#     query = query.order("month_curr", desc=(sort_order == "desc"))

#     # Execute and build dataframe
#     try:
#         result = query.execute()
#         df = pd.DataFrame(result.data)
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

#     if df.empty:
#         return Response({"error": "No data found for this HS code"}, status=404)

#     # Optional month filtering
#     if month_from:
#         df = df[df['month_curr'] >= month_from]
#     if month_to:
#         df = df[df['month_curr'] <= month_to]

#     # Apply limit at the end
#     df = df.head(limit)

#     # Format response
#     df = df[["month_curr", "value_curr", "value_unit", "commodity", "growth_pct"]]
#     return Response(df.to_dict(orient="records"))



from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..supabase_client import supabase
import pandas as pd

@api_view(['GET'])
def export_data_view(request):
    hs_code = request.GET.get("hs_code")
    if not hs_code:
        return Response({"error": "Missing 'hs_code' parameter."}, status=400)

    # Optional parameters
    try:
        limit = int(request.GET.get("limit", 12))
        if limit <= 0:
            raise ValueError
    except ValueError:
        return Response({"error": "'limit' must be a positive integer."}, status=400)

    sort_order = request.GET.get("sort", "asc").lower()
    if sort_order not in ["asc", "desc"]:
        return Response({"error": "Invalid 'sort' value. Use 'asc' or 'desc'."}, status=400)

    # Query Supabase
    try:
        query = supabase.table("monthly_exports").select("*").eq("hs_code", hs_code)
        query = query.order("month_curr", desc=(sort_order == "desc")).limit(limit)
        res = query.execute()
        df = pd.DataFrame(res.data)
    except Exception as e:
        return Response({"error": f"Failed to fetch data: {str(e)}"}, status=500)

    if df.empty:
        return Response({"error": f"No data found for HS code {hs_code}."}, status=404)

    # Format nicely for frontend
    result = df[[
        "month_curr", "value_curr", "value_unit", "commodity", "growth_pct"
    ]].sort_values("month_curr")  # Ensures chronological order on frontend

    return Response(result.to_dict(orient="records"))
