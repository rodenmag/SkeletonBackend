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
from rest_framework.decorators import action

from django.core.cache import cache
#from django.utils.decorators import method_decorator
#from django.views.decorators.cache import cache_page
#from django.utils.cache import get_cache_key


from rest_framework.views import APIView
from .services import compare_documents

from django.db.models import Q, Value
from django.db.models.functions import Concat
from .tasks import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.contrib.auth.models import User

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class AutoCompleteStandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class ActivityFilterSet(FilterSet):
    id = filters.CharFilter('id')
    function = filters.CharFilter('function')
    subject = filters.CharFilter('subject')
    content_text = filters.CharFilter('content_text')
    approval_status = filters.CharFilter('approval_status')
    document_type = filters.CharFilter('document_type')
    revision_number = filters.CharFilter('revision_number')
    board_resolution_number = filters.CharFilter('board_resolution_number')
    related_board_resolution_number = filters.CharFilter('related_board_resolution_number')
    department = filters.CharFilter('department')
    status = filters.CharFilter('status')
    date_issued_gte = filters.DateFilter(field_name='date_issued', lookup_expr='gte')
    date_issued_lte = filters.DateFilter(field_name='date_issued', lookup_expr='lte')
    approval_user = filters.NumberFilter(field_name='approval__id', lookup_expr='exact')
    posted_by = filters.CharFilter('posted_by')
    public_viewer = filters.CharFilter('public_viewer')
    department_viewers = filters.NumberFilter(field_name='department_viewer__id', lookup_expr='exact')
    specific_viewers = filters.NumberFilter(field_name='specific_viewer__id', lookup_expr='exact')

    search = filters.CharFilter(
        field_name='content_text',
        lookup_expr='icontains'
    )
    search_subject = filters.CharFilter(
        field_name='subject',
        lookup_expr='icontains'
    )

    class Meta:
        model = Activity
        fields = (
            'id', 'subject', 'content_text', 'approval_status', 'document_type', 
            'revision_number', 'board_resolution_number', 'related_board_resolution_number', 
            'department', 'status', 'date_issued_gte', 'date_issued_lte', 'search_subject', 'search',
            'approval_user', 'posted_by', 'public_viewer', 'department_viewers', 'specific_viewers', 'function',
        )

class ActivityCrudViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivityCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #search_fields = ('subject',) 
    ordering_fields = '__all__'
    filterset_class = ActivityFilterSet

class DocumentTypeCrudViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('name',) 
    ordering_fields = '__all__'

class DocumentTypeOptionViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeOptionSerializer

class DocumentFileFilterSet(FilterSet):
    id = filters.CharFilter('id')
    subject = filters.CharFilter('subject')
    content_text = filters.CharFilter('content_text')
    approval_status = filters.CharFilter('approval_status')
    document_type = filters.CharFilter('document_type')
    revision_number = filters.CharFilter('revision_number')
    board_resolution_number = filters.CharFilter('board_resolution_number')
    related_board_resolution_number = filters.CharFilter('related_board_resolution_number')
    department = filters.CharFilter('department')
    status = filters.CharFilter('status')
    date_issued_gte = filters.DateFilter(field_name='date_issued', lookup_expr='gte')
    date_issued_lte = filters.DateFilter(field_name='date_issued', lookup_expr='lte')
    approval_user = filters.NumberFilter(field_name='approval__id', lookup_expr='exact')
    posted_by = filters.CharFilter('posted_by')
    public_viewer = filters.CharFilter('public_viewer')
    department_viewers = filters.NumberFilter(field_name='department_viewer__id', lookup_expr='exact')
    specific_viewers = filters.NumberFilter(field_name='specific_viewer__id', lookup_expr='exact')

    search = filters.CharFilter(
        field_name='content_text',
        lookup_expr='icontains'
    )
    search_subject = filters.CharFilter(
        field_name='subject',
        lookup_expr='icontains'
    )

    class Meta:
        model = DocumentFile
        fields = (
            'id', 'subject', 'content_text', 'approval_status', 'document_type', 
            'revision_number', 'board_resolution_number', 'related_board_resolution_number', 
            'department', 'status', 'date_issued_gte', 'date_issued_lte', 'search_subject', 'search',
            'approval_user', 'posted_by', 'public_viewer', 'department_viewers', 'specific_viewers',
        )



class DocumentFileCrudViewSet(viewsets.ModelViewSet):
    queryset = DocumentFile.objects.all()
    serializer_class = DocumentFileCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #search_fields = ('content_text',)  # Define fields to search
    ordering_fields = '__all__'
    filterset_class = DocumentFileFilterSet

    def view_document(self, request, pk=None):

        instance = self.get_object()

        activity_post_async.delay(
            instance.id,
            'View',
            (
                f"{request.user.first_name} "
                f"{request.user.last_name}"
            ).strip() or request.user.username
        )

        return Response({
            'detail': 'View logged'
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, "user_profile", None)
        department = profile.department_id
        full_name = f"{user.first_name} {user.last_name}"

        queryset = DocumentFile.objects.filter(
            Q(public_viewer=True) |
                (
                    Q(posted_by=full_name) |
                    Q(specific_viewer=user) |
                    Q(department_viewer=department) |
                    Q(approval=user) |
                    Q(group_viewer__group__user_id=user.pk)
                )
        ).distinct()

        return queryset

    def perform_create(self, serializer):
        doc = serializer.save()

        extract_document_text_async.delay(doc.id)

        activity_post_async.delay(
            doc.id,
            'Create',
            (
                f"{self.request.user.first_name} "
                f"{self.request.user.last_name}"
            ).strip() or self.request.user.username
        )
        send_for_approval_notifications.delay(doc.id)

    def perform_update(self, serializer):
        instance = self.get_object()

        old_file = instance.file
        old_status = instance.status
        old_approval_status = instance.approval_status

        doc = serializer.save()

        # Re-extract text if file changed
        if "file" in serializer.validated_data:
            if old_file != doc.file:
                extract_document_text_async.delay(doc.id)

        # Default activity
        activity_function = 'Update'

        # Approval status changed
        if (
            "approval_status" in serializer.validated_data and
            old_approval_status != doc.approval_status
        ):

            # If Pending, keep as Update
            if doc.approval_status != 'Pending':
                activity_function = doc.approval_status

        # Status changed
        elif (
            "status" in serializer.validated_data and
            old_status != doc.status
        ):

            # If Pending, keep as Update
            if doc.status != 'Pending':
                activity_function = doc.status

        activity_post_async.delay(
            doc.id,
            activity_function,
            (
                f"{self.request.user.first_name} "
                f"{self.request.user.last_name}"
            ).strip() or self.request.user.username
        )

        if doc.status == 'Pending':
            send_for_approval_notifications.delay(doc.id)
        

    def perform_destroy(self, instance):

        data = {
            'file_name': instance.file.name if instance.file else None,
            
            'function': 'Delete',
            'user': (
                f"{self.request.user.first_name} "
                f"{self.request.user.last_name}"
            ).strip() or self.request.user.username,

            'document_type': instance.document_type,
            'status': instance.status,
            'subject': instance.subject,
            'short_description': instance.short_description,
            'content_text': instance.content_text,
            'scanned': instance.scanned,
            'revision_number': instance.revision_number,
            'board_resolution_number': instance.board_resolution_number,
            'date_issued': str(instance.date_issued),
            'related_board_resolution_number': instance.related_board_resolution_number,
            'department_id': instance.department.id if instance.department else None,
            'approved_by': instance.approved_by,
            'posted_by': instance.posted_by,
            'date_posted': str(instance.date_posted) if instance.date_posted else None,
            'time_posted': str(instance.time_posted) if instance.time_posted else None,
            'approval_status': instance.approval_status,
            'public_viewer': instance.public_viewer,

            # many-to-many
            'approval_ids': list(instance.approval.values_list('id', flat=True)),
            'department_viewer_ids': list(instance.department_viewer.values_list('id', flat=True)),
            'specific_viewer_ids': list(instance.specific_viewer.values_list('id', flat=True)),
        }

        activity_post_delete_async.delay(data)

        instance.delete()



class DocumentFileCrudAdminViewSet(viewsets.ModelViewSet):
    queryset = DocumentFile.objects.all()
    serializer_class = DocumentFileCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #search_fields = ('content_text',)  # Define fields to search
    ordering_fields = '__all__'
    filterset_class = DocumentFileFilterSet
    #filterset_fields = (
    #    'id', 'subject', 'content_text', 'approval_status', 
    #    'document_type', 'revision_number', 'board_resolution_number', 
    #    'related_board_resolution_number', 'department', 'status'
    #)

    def perform_create(self, serializer):
        doc = serializer.save()
        extract_document_text_async.delay(doc.id)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_file = instance.file

        doc = serializer.save()

        if "file" in serializer.validated_data:
            if old_file != doc.file:
                extract_document_text_async.delay(doc.id)




class CompareDocumentsView(APIView):
    def post(self, request):
        doc_a_id = request.data.get("doc_a")
        doc_b_id = request.data.get("doc_b")

        doc_a = DocumentFile.objects.get(id=doc_a_id)
        doc_b = DocumentFile.objects.get(id=doc_b_id)

        result = compare_documents(
            doc_a.content_text,
            doc_b.content_text
        )

        return Response({
            "comparison": result
        }, status=status.HTTP_200_OK)
        #{ "doc_a": 79, "doc_b": 80 }



#dashboard
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "Policy": DocumentFile.objects.filter(
                document_type__iexact="Policy",
                status__iexact="Active"
            ).count(),

            "Memo": DocumentFile.objects.filter(
                document_type__iexact="Memo",
                status__iexact="Active"
            ).count(),

            "Manual": DocumentFile.objects.filter(
                document_type__iexact="Manual",
                status__iexact="Active"
            ).count(),

            "MinutesOfMeeting": DocumentFile.objects.filter(
                document_type__iexact="Minutes of Meeting",
                status__iexact="Active"
            ).count(),

            "Contracts": DocumentFile.objects.filter(
                document_type__iexact="Contracts",
                status__iexact="Active"
            ).count(),

            # Status
            "Active": DocumentFile.objects.filter(
                status__iexact="Active"
            ).count(),

            "Archived": DocumentFile.objects.filter(
                status__iexact="Archived"
            ).count(),

            "ActiveUsers": User.objects.filter(
                is_active=True
            ).count(),
        }

        return Response(data)

#background task
class ActivityView(APIView):

    def post(self, request):

        data = {
            'subject': request.data.get('subject'),
            'document_type': request.data.get('document_type'),
            'function': request.data.get('function'),
            'user': request.data.get('user'),
        }

        activity_post_async.delay(data)

        return Response({
            'detail': 'Activity queued successfully'
        }, status=status.HTTP_200_OK)