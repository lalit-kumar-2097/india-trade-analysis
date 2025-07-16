from django.urls import path
from .views.forecast_view import forecast_view
from .views.export_data_view import export_data_view
from django.urls import path
from .views.commodities_view import search_commodities


urlpatterns = [
    path('forecast/', forecast_view),
    path("monthly-exports/", export_data_view, name="monthly-exports"),
    path('commodities/', search_commodities, name='search_commodities'),
]


# tradeapp/urls.py
# This file defines the URL patterns for the tradeapp application.
# It maps the 'forecast/' URL to the forecast_view function in views.py.
# It also maps the 'api/monthly-exports/' URL to the export_data_view function
# in views.py, which handles the export of monthly trade data.
# This file defines the URL patterns for the tradeapp application.
# It maps the 'forecast/' URL to the forecast_view function in views.py.
# This allows the application to handle requests for trade forecasts based on HS codes.
# The forecast_view function will process the request, fetch data from the Supabase database,
# and return the forecasted trade data as a response.
# Make sure to include this URL configuration in the main project's urls.py file.
# This is done by adding `path('api/', include('tradeapp.urls'))` in the main urls.py file.


