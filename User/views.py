from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Q, Value, Sum
from django.db.models.functions import Concat

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class AutoCompleteStandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 1000000

#custom user login
class ObtainCustomJWTView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]  # Allows unrestricted access
    def post(self, request):
        serializer = CustomJWTSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Create your views here.
def jwt_response_payload_handler(token, User=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(User, context={'request': request}).data
        #'user': SimpleUserSerializer(User, context={'request': request}).data
        #'permission': AuthPermissionSerializer(user, context={'request': request}).data
    }

class UserApproverAutocompleteIDAPIView(generics.ListAPIView):
    serializer_class = UserLabelValueIDSerializer
    pagination_class = AutoCompleteStandardResultsSetPagination
        
    def get_queryset(self):
        query = self.request.query_params.get("query", "").strip()
        
        # Base queryset: ensure always filter by approver=True
        base_qs = User.objects.filter(user_profile__approver=True)

        # If no search text, just return all approvers
        if not query:
            return base_qs

        # Annotate full names for flexible matching
        queryset = base_qs.annotate(
            first_name_first_full_name=Concat('first_name', Value(' '), 'last_name'),
            last_name_first_full_name=Concat('last_name', Value(' '), 'first_name')
        )

        # Search among endorsers only
        return queryset.filter(
            Q(first_name_first_full_name__icontains=query) |
            Q(last_name_first_full_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

class SimpleUserCrudViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SimpleUserCrudSerializer


class UserCrudViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('id', 'first_name', 'last_name', 'username')  # Define fields to search
    ordering_fields = '__all__'
    #filterset_fields = ('id', 'first_name', 'last_name', 'user_profile__branch_id', 'user_profile__department_id', 'user_profile__level_id', 'username', 'is_active', 'user_profile__endorser', 'user_profile__approver')
    filterset_fields = ('__all__')


class BranchCrudViewSet(viewsets.ModelViewSet): #CRUD Branch
    queryset = Branch.objects.all()
    serializer_class = BranchCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('id', 'name', 'code')
    ordering_fields = '__all__'
    filterset_fields = ('__all__')


class DepartmentCrudViewSet(viewsets.ModelViewSet): #CRUD Department
    queryset = Department.objects.all()
    serializer_class = DepartmentCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('id', 'name')
    ordering_fields = '__all__'
    filterset_fields = ('__all__')


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = AuthUserGroupsSerializer

class BranchAutocompleteAPIView(generics.ListAPIView):
    serializer_class = BranchLabelValueSerializer
    pagination_class = AutoCompleteStandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        #queryset = Client.objects.filter(last_name__icontains=query) | Client.objects.filter(first_name__icontains=query) | Client.objects.filter(middle_name__icontains=query)
        queryset = Branch.objects.filter((Q(name__icontains=query) | Q(code__icontains=query)))
        return queryset

class DepartmentAutocompleteAPIView(generics.ListAPIView):
    serializer_class = DepartmentLabelValueSerializer
    pagination_class = AutoCompleteStandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        #queryset = Client.objects.filter(last_name__icontains=query) | Client.objects.filter(first_name__icontains=query) | Client.objects.filter(middle_name__icontains=query)
        queryset = Department.objects.filter((Q(name__icontains=query)))
        return queryset

class GroupAutocompleteAPIView(generics.ListAPIView):
    serializer_class = GroupLabelValueSerializer
    pagination_class = AutoCompleteStandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        #queryset = Client.objects.filter(last_name__icontains=query) | Client.objects.filter(first_name__icontains=query) | Client.objects.filter(middle_name__icontains=query)
        queryset = MainGroup.objects.filter((Q(name__icontains=query)))
        return queryset

class UserAutocompleteIDAPIView(generics.ListAPIView):
    serializer_class = UserLabelValueIDSerializer
    pagination_class = AutoCompleteStandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get("query", "").strip()
        
        if not query:
            return User.objects.all()

        # Annotate a full_name field (first_name + last_name)
        queryset = User.objects.annotate(
            first_name_first_full_name=Concat('first_name', Value(' '), 'last_name'),
            last_name_first_full_name=Concat('last_name', Value(' '), 'first_name')
        )

        # Search against full_name for more flexibility
        return queryset.filter(Q(first_name_first_full_name__icontains=query) | Q(last_name_first_full_name__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))


class BranchFilterView(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchLabelValueSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', )

class GroupFilterView(generics.ListAPIView):
    queryset = MainGroup.objects.all()
    serializer_class = GroupLabelValueSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', )

class DepartmentFilterView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentLabelValueSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', )

class UserFilterView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLabelValueIDSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', )

class UserDataFilterView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', )


class GroupGoogleViewSet(viewsets.ModelViewSet):
    queryset = MainGroup.objects.all()
    serializer_class = GroupCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ('name',)

#class GroupEmailViewSet(viewsets.ModelViewSet):
#    queryset = GroupEmail.objects.all()
#    serializer_class = GroupEmailCrudSerializer
#    pagination_class = StandardResultsSetPagination
#    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#    ordering_fields = '__all__'
#    filterset_fields = ('name', 'email', 'group')

#class GroupEmailFilterView(generics.ListAPIView):
#    queryset = GroupEmail.objects.all()
#    serializer_class = GroupEmailCrudSerializer
#    filter_backends = (DjangoFilterBackend,)
#    filterset_fields = ('id', 'group',)


class GroupUserViewSet(viewsets.ModelViewSet):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserCrudSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('name',)
    ordering_fields = '__all__'
    filterset_fields = ('name', 'email', 'group_id')

class GroupUserFilterView(generics.ListAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserCrudSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filterset_fields = ('id', 'group_id',)
