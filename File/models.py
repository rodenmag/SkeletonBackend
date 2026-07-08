import os
from django.db import models
from django.contrib.auth.models import User
from User.models import *
from django.dispatch import receiver
# Create your models here.
class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    date_posted = models.DateField()
    posted_by = models.CharField(max_length=100)


class Activity(models.Model):
    function = models.CharField(max_length=200) #view, create, update, delete, approved, denied
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.CharField(max_length=200)
    file_name = models.CharField(max_length=500, null=True, blank=True)

    document_type = models.CharField(max_length=50, null=True, blank=True) #(policy, memo, others) /
    status = models.CharField(max_length=50, default='Active') #Active, Archived /
    subject = models.CharField(max_length=500) #/
    short_description = models.CharField(max_length=200, null=True, blank=True) #/
    content_text = models.TextField(blank=True) #/
    scanned = models.BooleanField(default=False) #/
    revision_number = models.IntegerField(default=1) #/
    board_resolution_number = models.CharField(max_length=200, null=True, blank=True) #/
    date_issued = models.DateField() #/
    related_board_resolution_number = models.CharField(max_length=200, null=True, blank=True) #/
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='document_file_department_activity')
    approved_by = models.CharField(max_length=100, null=True, blank=True)
    posted_by = models.CharField(max_length=100, null=True, blank=True)
    date_posted = models.DateField(null=True, blank=True)
    time_posted = models.TimeField(null=True, blank=True)
    approval = models.ManyToManyField(User, blank=True, related_name='document_file_approval_activity')
    approval_status = models.CharField(max_length=50, default='Pending') #Cancelled, Pending, Denied, Approved
    public_viewer = models.BooleanField(default=False)
    department_viewer = models.ManyToManyField(Department, blank=True, related_name='document_file_department_viewer_activity')
    specific_viewer = models.ManyToManyField(User, blank=True, related_name='document_file_specific_viewer_activity')
    group_viewer = models.ManyToManyField(MainGroup, blank=True, related_name='document_file_group_viewer_activity')


class DocumentFile(models.Model):
    document_type = models.CharField(max_length=50, null=True, blank=True) #(policy, memo, others) /
    status = models.CharField(max_length=50, default='Active') #Active, Archived, Deleted/
    subject = models.CharField(max_length=500) #/
    short_description = models.CharField(max_length=200, null=True, blank=True) #/
    content_text = models.TextField(blank=True) #/
    file = models.FileField(upload_to="pdfs/", null=True, blank=True) #/
    scanned = models.BooleanField(default=False) #/
    revision_number = models.IntegerField(default=1) #/
    board_resolution_number = models.CharField(max_length=200, null=True, blank=True) #/
    date_issued = models.DateField() #/
    related_board_resolution_number = models.CharField(max_length=200, null=True, blank=True) #/
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='document_file_department')
    approved_by = models.CharField(max_length=100, null=True, blank=True)
    posted_by = models.CharField(max_length=100, null=True, blank=True)
    date_posted = models.DateField(null=True, blank=True)
    time_posted = models.TimeField(null=True, blank=True)
    approval = models.ManyToManyField(User, blank=True, related_name='document_file_approval')
    approval_status = models.CharField(max_length=50, default='Pending') #Cancelled, Pending, Denied, Approved
    public_viewer = models.BooleanField(default=False)
    department_viewer = models.ManyToManyField(Department, blank=True, related_name='document_file_department_viewer')
    specific_viewer = models.ManyToManyField(User, blank=True, related_name='document_file_specific_viewer')
    group_viewer = models.ManyToManyField(MainGroup, blank=True, related_name='document_groups')

@receiver(models.signals.post_delete, sender=DocumentFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=DocumentFile)
def auto_delete_file_on_change(sender, instance, **kwargs):

    # New object, no old file yet
    if not instance.pk:
        return False

    try:
        old_file = DocumentFile.objects.get(pk=instance.pk).file
    except DocumentFile.DoesNotExist:
        return False

    new_file = instance.file

    # No old file
    if not old_file:
        return False

    # File changed
    if old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    """
    def save(self, *args, **kwargs):
        if self.pk:
            old = DocumentFile.objects.filter(pk=self.pk).first()
            if old and old.file and old.file != self.file:
                if os.path.isfile(old.file.path):
                    os.remove(old.file.path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)
    """


"""
class DocumentAuditLog(models.model):
    subject = models.CharField(max_length=500)
    user = models.CharField(max_length=100, null=True, blank=True)
    action  = models.CharField(max_length=25)#(viewed, downloaded, approved, archived)
    date_posted = models.DateField(null=True, blank=True)
    time_posted = models.TimeField(null=True, blank=True)
"""