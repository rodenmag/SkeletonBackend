from django.contrib import admin
from .models import *
admin.site.register(DocumentType)
admin.site.register(DocumentFile)
admin.site.register(Activity)