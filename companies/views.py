from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Company
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import CompanySerializer
from rest_framework.pagination import PageNumberPagination


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_updated")
    pagination_class = PageNumberPagination

'''send company emails'''
@api_view(http_method_names=['POST'])
def send_company_email():
    send_mail(subject='My cool subject', message='My cool message', from_email='okidijimmie@gmail.com', recipient_list='okidijimmie@gmail.com')
    return Response({'status': 'success', 'info': 'email sent successfully'}, status=200)