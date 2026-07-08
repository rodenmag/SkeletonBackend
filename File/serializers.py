# serializers.py
from rest_framework import serializers
from .models import *
from .tasks import extract_document_text_async

class ActivityCrudSerializer(serializers.ModelSerializer):
    #file = serializers.FileField(required=False, allow_null=True)
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = "__all__"

    def get_department_name(self, obj):
        try:
            qs =  obj.department.name
            return qs
        except Exception as ex:
            return None

class DocumentFileCrudSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = DocumentFile
        fields = "__all__"

    def get_department_name(self, obj):
        try:
            qs =  obj.department.name
            return qs
        except Exception as ex:
            return None

    def validate(self, attrs):
        subject = attrs.get(
            'subject',
            getattr(self.instance, 'subject', None)
        )

        status = attrs.get(
            'status',
            getattr(self.instance, 'status', None)
        )

        # Only enforce uniqueness for Active documents
        if status != 'Active':
            return attrs

        qs = DocumentFile.objects.filter(
            subject__iexact=subject.strip(),
            status='Active'
        )

        # Exclude current record during update
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError({
                'subject': 'An active document with the same subject already exists.'
            })

        return attrs

class DocumentTypeCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = "__all__"

class DocumentTypeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('name', )
