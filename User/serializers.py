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
from django.contrib.auth import authenticate

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework_jwt.settings import api_settings
User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserLabelValueIDSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('label', 'value') #, 'first_name', 'middle_name', 'last_name')

    def get_label(self, obj):
        try:
            qs = obj.last_name + ', ' + obj.first_name
            return qs
        except Exception as ex:
            return None

    def get_value(self, obj):
        try:
            qs = obj.id
            return qs
        except Exception as ex:
            return None

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__') #, 'first_name', 'middle_name', 'last_name')
            
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user_page', 'uploader', 'approver', 'branch_id', 'department_id', 'ai_helper', 'employee_id', 'admin_uploader', 'logs')

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
        instance.is_active = validated_data.get('is_active', instance.is_active)
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
    #admin_access = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    user_page = serializers.SerializerMethodField()
    uploader = serializers.SerializerMethodField()
    approver = serializers.SerializerMethodField()
    ai_helper = serializers.SerializerMethodField()
    employee_number = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'user_profile', 'password', 'last_login', 'is_superuser', 
            'username', 'first_name', 'last_name', 'email', 'is_staff', 
            'is_active', 'groups', 'group_names', 'branch', 'department', 
            'user_page', 'approver', 'uploader', 'ai_helper', 'employee_number',
        )
    
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

    #def get_admin_access(self, obj):
    #    try:
    #        qs =  obj.user_profile.admin_access
    #        return qs
    #    except Exception as ex:
    #        return None
    def get_user_page(self, obj):
        try:
            qs =  obj.user_profile.user_page
            return qs
        except Exception as ex:
            return None
            
    def get_uploader(self, obj):
        try:
            qs =  obj.user_profile.uploader
            return qs
        except Exception as ex:
            return None

    def get_approver(self, obj):
        try:
            qs =  obj.user_profile.approver
            return qs
        except Exception as ex:
            return None

    def get_department(self, obj):
        try:
            qs =  obj.user_profile.department_id.name
            return qs
        except Exception as ex:
            return None

    def get_branch(self, obj):
        try:
            qs =  obj.user_profile.branch_id.name
            return qs
        except Exception as ex:
            return None

    def get_ai_helper(self, obj):
        try:
            qs =  obj.user_profile.ai_helper
            return qs
        except Exception as ex:
            return None

    def get_employee_number(self, obj):
        try:
            qs =  obj.user_profile.employee_id
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

class BranchCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'code', 'status')

class DepartmentCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'status')

class BranchLabelValueSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ('label', 'value')

    def get_label(self, obj):
        try:
            qs = obj.name
            return qs
        except Exception as ex:
            return None

    def get_value(self, obj):
        try:
            qs = obj.id
            return qs
        except Exception as ex:
            return None

class DepartmentLabelValueSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ('label', 'value')

    def get_label(self, obj):
        try:
            qs = obj.name
            return qs
        except Exception as ex:
            return None

    def get_value(self, obj):
        try:
            qs = obj.id
            return qs
        except Exception as ex:
            return None

class GroupLabelValueSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    class Meta:
        model = MainGroup
        fields = ('label', 'value')

    def get_label(self, obj):
        try:
            qs = obj.name
            return qs
        except Exception as ex:
            return None

    def get_value(self, obj):
        try:
            qs = obj.id
            return qs
        except Exception as ex:
            return None

class UserLabelValueIDSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('label', 'value') #, 'first_name', 'middle_name', 'last_name')

    def get_label(self, obj):
        try:
            qs = obj.last_name + ', ' + obj.first_name
            return qs
        except Exception as ex:
            return None

    def get_value(self, obj):
        try:
            qs = obj.id
            return qs
        except Exception as ex:
            return None


#custom user login
class CustomJWTSerializer(serializers.Serializer):
    username_field = 'username'
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("username") + '@qcrblive.com').first() or \
                   User.objects.filter(username=attrs.get("username")).first()

        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        raise serializers.ValidationError(_('User account is disabled.'))
                    
                    # Generate JWT Token
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                    payload = jwt_payload_handler(user)  # Create token payload
                    token = jwt_encode_handler(payload)  # Encode token

                    return {
                        'token': token,  # Add token in the response
                        'user': UserSerializer(user).data
                    }
                else:
                    if not user_obj.is_active:
                        # Explicitly tell them account is disabled
                        raise serializers.ValidationError(_('User account is disabled.'))
                    else:
                        # User exists but wrong password
                        raise serializers.ValidationError(_('Invalid username or password.'))
            else:
                raise serializers.ValidationError(_('Both username and password are required.'))
        else:
            raise serializers.ValidationError(_('User not found.'))


#Group
class GroupCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
    name = serializers.CharField()
    
class GroupCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainGroup
        fields = "__all__"


#class GroupEmailCrudSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = GroupEmail
#        fields = "__all__"


class GroupUserCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = "__all__"