from django.db import models

# Create your models here.

class Document(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=500)
    content_text = models.TextField(blank=True)
    file = models.FileField(upload_to="pdfs/")
    scanned = models.BooleanField()
