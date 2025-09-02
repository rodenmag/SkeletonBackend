__author__ = 'Roden Magat'
from .models import *
from .serializers import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
import django_filters
import math
import logging
from django.db.models import Q
from django.db.models import Sum

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('position')

class SimpleUserCrudSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'user_profile', 'first_name', 'last_name', 'email', 'groups', 'is_staff', 'is_active', 'is_superuser')

    def update(self, instance, validated_data):
        user_profile_data = validated_data.pop('user_profile', None)
        groups_data = validated_data.pop('groups', None)
        if user_profile_data:
            user_profile = instance.user_profile

            # Update each field in user_profile if provided
            for attr, value in user_profile_data.items():
                setattr(user_profile, attr, value)
            user_profile.save()

        # Update user fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        if groups_data is not None:
            instance.groups.set(groups_data)
        instance.save()

        return instance



class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    #password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    email = serializers.CharField(required=True, max_length=30)
    group_names = serializers.SerializerMethodField()
    #branch_code = serializers.SerializerMethodField()
    #contact_number = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    #user_group_name = serializers.ReadOnlyField(source='user_group.name')
    #user_group_name = serializers.RelatedField(source='groups', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'user_profile', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups', 'group_names', 'position')
    def create(self, validated_data):
        profile_data = validated_data.pop('user_profile', None)
        groups_data = validated_data.pop('groups', [])
        #user = super(UserSerializer, self).create(validated_data)
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        if groups_data:
            user.groups.set(groups_data)
        return user
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user_profile', None)
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)  # Exclude password from validated_data

        # Update fields of the User instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password if included
        if password:
            instance.set_password(password)

        instance.save()

        # Update associated profile data
        if profile_data:
            profile = instance.user_profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        # Update associated groups
        if groups_data is not None:
            instance.groups.set(groups_data)

        return instance
    def get_group_names(self, obj):
        group_ids = obj.groups.all()
        group_names = Group.objects.filter(id__in=group_ids).values_list('name', flat=True)
        return group_names
    def get_position(self, obj):
        try:
            qs =  obj.user_profile.position
            return qs
        except Exception as ex:
            return None
    
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_staff', 'is_active', 'groups')

class AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('__all__')

class AuthUserGroupsSerializer(serializers.ModelSerializer):
    #user_permission = AuthPermissionSerializer(source='permissions', read_only=True, many=True)
    class Meta:
        model = Group
        fields = ('id', 'name')#, 'permissions', 'user_permission')