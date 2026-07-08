# serializers.py
from rest_framework import serializers
from .models import Document
from .tasks import extract_document_text_async

class DocumentCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

    #def create(self, validated_data):
    #    doc = super().create(validated_data)
    #    extract_document_text_async.delay(doc.id)
    #    return doc