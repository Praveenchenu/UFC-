from django.shortcuts import render
from muaithai.models import Fighter_Details
from muaithai.serializers import FightersSerializer
from rest_framework import viewsets, permissions, filters

class Fighters_CRUD_api_View(viewsets.ModelViewSet):
    queryset = Fighter_Details.objects.all()
    serializer_class = FightersSerializer

    permission_class = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Name', 'Weight_class', 'Age', 'p4p_rank']
    ordering_fields = ['Weight_class']
