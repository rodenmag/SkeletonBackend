from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework import views
from rest_framework import status
from datetime import date, datetime
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from django.core.cache import cache
#from django.utils.decorators import method_decorator
#from django.views.decorators.cache import cache_page
#from django.utils.cache import get_cache_key

from django.db.models import Q, Value
from django.db.models.functions import Concat
from .tasks import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class AutoCompleteStandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class DocumentCrudViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('name', 'last_name', 'content_text')  # Define fields to search
    ordering_fields = '__all__'
    filterset_fields = ('id',)

    def perform_create(self, serializer):
        doc = serializer.save()
        # 🔥 Side-effect belongs here, not serializer
        #extract_document_text_async.delay(doc.id)
        extract_document_text_async.delay()