from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from store.api.serializers import MpesaPaymentSerializer
from store.models import MpesaPayment
import json
import requests
from requests.auth import HTTPBasicAuth
from store.mpesa_credentials import MpesaAccessToken,LipaNaMpesaPassword


@api_view(['GET'])
@csrf_exempt
def api_register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.test_c2b_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://26305433cb94.ngrok.io/api/c2b/confirmation/",
               "ValidationURL": "https://26305433cb94.ngrok.io/api/c2b/validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return Response(response.text)

@api_view(['GET'])
@csrf_exempt
def api_call_back(request):
    pass

@api_view(['GET'])
@csrf_exempt
def api_validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return Response(dict(context))

@api_view(['GET'])
@csrf_exempt
def api_confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return Response(dict(context))