from django.urls import path
from .views import *

app_name = 'store'


urlpatterns = [
    path('', IndexView, name="index"),
    path('shop/', Shop, name='shop'),
    path('products/category/<slug>', ItemCategoryView, name='category-list' ),
    path('add-to-cart/<slug>/', AddToCart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', RemoveFromCart, name='remove-from-cart'),
    path('add-to-wishlist/<slug>/', AddToWish, name='add-to-wishlist'),
    path('contact/', ContactView, name='contact'),
    path('about/', About, name='about'),
    path('cart/', CartView, name='cart'),
        
    #mpesa urls#
    path('checkout/lipa-na-mpesa/', MpesaPaymentView, name='lipa-na-mpesa'),
    path('c2b/register', register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', confirmation, name="confirmation"),
    path('c2b/validation', validation, name="validation"),
    path('c2b/callback', call_back, name="call_back"),
]
    