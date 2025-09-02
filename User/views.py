from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *

# Create your views here.
def jwt_response_payload_handler(token, User=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(User, context={'request': request}).data
        #'user': SimpleUserSerializer(user, context={'request': request}).data
        #'permission': AuthPermissionSerializer(user, context={'request': request}).data
    }

class SimpleUserCrudViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SimpleUserCrudSerializer


class UserCrudViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = AuthUserGroupsSerializer