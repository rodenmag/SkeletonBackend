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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class AutoCompleteStandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000


#autocomplete
class StudentAutocompleteAPIView(generics.ListAPIView):
    serializer_class = StudentLabelValueSerializer
    pagination_class = AutoCompleteStandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get("query", "").strip()
        
        if not query:
            return Student.objects.all()

        # Annotate a full_name field (first_name + last_name)
        queryset = Student.objects.annotate(
            first_name_first_full_name=Concat('first_name', Value(' '), 'last_name'),
            last_name_first_full_name=Concat('last_name', Value(' '), 'first_name')
        )

        # Search against full_name for more flexibility
        return queryset.filter(Q(first_name_first_full_name__icontains=query) | Q(last_name_first_full_name__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

# Create your views here.
class StudentRFIDFilterView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRFIDSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'rfid_number', 'student_id')

# Create your views here.
class StudentFilterView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentLabelValueSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'rfid_number', 'student_id')

class StudentCrudViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('first_name', 'middle_name', 'last_name', 'student_id', 'rfid_number')  # Define fields to search
    ordering_fields = '__all__'
    filterset_fields = ('id',)
    
class StudentLabelValueViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentLabelValueSerializer
