from store.api.views import (api_validation, 
                             api_confirmation, 
                             api_call_back, 
                             api_register_urls)
from django.urls import path

app_name='api'

urlpatterns = [
    path('c2b/register/', api_register_urls, name="api_register_mpesa_validation"),
    path('c2b/confirmation/', api_confirmation, name="api_confirmation"),
    path('c2b/validation/', api_validation, name="api_validation"),
    path('c2b/callback/', api_call_back, name="api_call_back"),
]
