from django.urls import path
from .views import *

app_name = 'store'


urlpatterns = [
    path('', IndexView, name="index"),
    path('contact/', ContactView, name='contact'),
    path('cart/', CartView, name='cart'),
]
    