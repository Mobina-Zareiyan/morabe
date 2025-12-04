from django.shortcuts import render
from rest_framework import generics, permissions


from .models import Contractor, RegistrationContractor
from .serializers import ContractorListSerializer, ContractorSerializer, RegistrationContractorSerializer


class ContractorListAPIView(generics.ListAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorListSerializer


class ContractorDetailAPIView(generics.RetrieveAPIView):
    queryset = Contractor.objects.prefetch_related('projects', 'galleries')
    serializer_class = ContractorSerializer
    lookup_field = 'slug'


class RegistrationAPIView(generics.CreateAPIView):
    queryset = RegistrationContractor.objects.all()
    serializer_class = RegistrationContractorSerializer
    permission_classes = [permissions.IsAuthenticated]


