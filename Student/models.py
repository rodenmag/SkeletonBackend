from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os

class Student(models.Model):
  student_id = models.CharField(max_length=150, null=True, blank=True)
  first_name = models.CharField(max_length=150)
  middle_name = models.CharField(max_length=150, null=True, blank=True)
  last_name = models.CharField(max_length=150)
  nickname = models.CharField(max_length=150, null=True, blank=True)
  birthday = models.DateField()
  citizenship = models.CharField(max_length=150, null=True, blank=True)
  religion = models.CharField(max_length=150, null=True, blank=True)
  address = models.CharField(max_length=1000, null=True, blank=True)
  email_address = models.CharField(max_length=150, null=True, blank=True)
  telephone_number = models.CharField(max_length=150, null=True, blank=True)
  mobile_number = models.CharField(max_length=150, null=True, blank=True)
  rfid_number = models.CharField(max_length=150, null=True, blank=True)
  #photo = models.ImageField(upload_to='Images/', default='Images/None/No0img.jpg')
  date_posted = models.DateField(null=True, blank=True)
  time_posted = models.TimeField(null=True, blank=True)
  posted_by = models.CharField(max_length=50, null=True, blank=True)

  father_name = models.CharField(max_length=250, null=True, blank=True)
  mother_name = models.CharField(max_length=250, null=True, blank=True)
  
# These two auto-delete files from filesystem when they are unneeded:
#@receiver(models.signals.post_delete, sender=Student)
#def auto_delete_file_on_delete(sender, instance, **kwargs):
#    """
#    Deletes file from filesystem
#    when corresponding `MediaFile` object is deleted.
#    """
#    if instance.photo:
#        if os.path.isfile(instance.photo.path):
#            os.remove(instance.photo.path)

#@receiver(models.signals.pre_save, sender=Student)
#def auto_delete_file_on_change(sender, instance, **kwargs):
#    """
#    Deletes old file from filesystem
#    when corresponding `MediaFile` object is updated
#    with new file.
#    """
#    if not instance.pk:
#        return False