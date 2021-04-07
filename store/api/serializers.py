from rest_framework import serializers
from store.models import Item, MpesaPayment

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name','category','description','new_price','pic_thumbnail']
        
class MpesaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = ['amount','description','type','reference','first_name','middle_name','last_name','phone_number','organization_balance']