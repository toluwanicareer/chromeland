from django.shortcuts import render
from django.views.generic import View
from .models import Company
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import pdb

# Create your views here.

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_data(request):
    code = request.GET['code']
    qid = request.GET['company']
    try:
        company = Company.objects.get(qid=qid)
    except :
        return Response({'detail': 'Not Found'}, status=HTTP_404_NOT_FOUND)

    try:
        result = company.scrape(code)
        return Response(result, status=HTTP_200_OK)
    except:
        return Response({'detail': 'Error In Processing,Please check your tracking ID, if problem persist contact Admin '}, status=HTTP_400_BAD_REQUEST)





