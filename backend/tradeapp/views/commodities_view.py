from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..supabase_client import supabase
import pandas as pd

@api_view(['GET'])
def search_commodities(request):
    search_query = request.GET.get('search', '').lower()

    if not search_query:
        return Response({"error": "Missing search parameter."}, status=400)

    # Fetch filtered data from Supabase
    response = supabase.table("commodities") \
        .select("hs_code, commodity") \
        .ilike("commodity", f"%{search_query}%") \
        .limit(20) \
        .execute()

    results = response.data

    # Optional: fallback to hs_code search if commodity name search returns empty
    if not results:
        response = supabase.table("commodities") \
            .select("hs_code, commodity") \
            .ilike("hs_code", f"%{search_query}%") \
            .limit(20) \
            .execute()
        results = response.data

    return Response(results)
