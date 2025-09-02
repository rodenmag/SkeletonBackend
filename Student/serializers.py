__author__ = 'Roden Magat'
from .models import *
from .serializers import *
from rest_framework import serializers
from datetime import date, datetime


class StudentRFIDSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ('full_name', 'student_id', 'rfid_number')#, 'photo')
    
    def get_full_name(self, obj):
        try:
            mname = obj.middle_name
            if mname == None:
                mname = ''
            qs = obj.first_name + ' ' + mname + ' ' + obj.last_name
            return qs
        except Exception as ex:
            return None

class StudentCrudSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ('__all__')
    
    def get_full_name(self, obj):
        try:
            mname = obj.middle_name
            if mname == None:
                mname = ''
            qs = obj.first_name + ' ' + mname + ' ' + obj.last_name
            return qs
        except Exception as ex:
            return None

class StudentLabelValueSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ('label', 'value') #, 'first_name', 'middle_name', 'last_name')

    def get_label(self, obj):
        try:
            mname = obj.middle_name
            if mname == None:
                mname = ''
            qs = obj.first_name + ' ' + mname + ' ' + obj.last_name
            return qs
        except Exception as ex:
            return None

    def get_value(self, obj):
        try:
            qs = obj.id
            return qs
        except Exception as ex:
            return None
        
