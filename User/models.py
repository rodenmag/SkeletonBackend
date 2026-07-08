from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

#temporary for migrations
#class Level(models.Model):
#    name = models.CharField(max_length=100)
#    description = models.CharField(max_length=100)


class MainGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    #status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#class GroupEmail(models.Model):
#    group = models.ForeignKey(
#        MainGroup,
#        on_delete=models.CASCADE,
#        related_name='emails'
#    )
#    name = models.CharField(max_length=100)
#    email = models.EmailField()
#    def __str__(self):
#        return self.email

class GroupUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_user')
    group_id = models.ForeignKey(MainGroup, on_delete=models.CASCADE, related_name='group')
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)

class Branch(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    #def __str__(self):
    #    return self.name

class Department(models.Model):
    name = models.CharField(max_length=50)
    #code = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    #def __str__(self):
    #    return self.name

"""
class new_employee_level(models.Model):
	name = models.CharField(max_length=100)
	order = models.IntegerField()
	posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
	date_posted = models.DateField()
"""

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    user_page = models.BooleanField(default=False) #new
    uploader = models.BooleanField(default=False) #new
    approver = models.BooleanField(default=False)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    ai_helper = models.BooleanField(default=False) #new
    admin_uploader = models.BooleanField(default=False)
    logs = models.BooleanField(default=False)
    #level = models.CharField(max_length=100, blank=True, null=True)


    #temporary for migration
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    admin_access = models.CharField(max_length=10, default='none') #hr or it
    manual_in_out = models.BooleanField(default=False)
    salary_per_day = models.FloatField(default=0)
    salary_per_month = models.FloatField(default=0)
    permanency_date = models.DateField(blank=True, null=True)
    vacation_leave = models.FloatField(default=10)
    sick_leave = models.FloatField(default=10)
    forced_leave = models.FloatField(default=5)
    maternity_leave = models.FloatField(default=105)
    paternity_leave = models.FloatField(default=7)
    solo_parent_leave = models.FloatField(default=7)
    magna_carta_leave = models.FloatField(default=60)
    vawc_leave = models.FloatField(default=10)
    lwop = models.FloatField(default=0)
    service_incentive_leave = models.FloatField(default=5)
    covid_leave = models.FloatField(default=5)
    employee_panel_calendar = models.BooleanField(default=False)
    department_attendance = models.BooleanField(default=False)

    schedule_in = models.TimeField(blank=True, null=True)
    schedule_out = models.TimeField(blank=True, null=True)
    
    endorser = models.BooleanField(default=False)
    approver = models.BooleanField(default=False)
    """

    #approver = models.BooleanField(default=False)

#python manage.py dumpdata auth.user User.UserProfile --indent 4 > users.json
#python manage.py dumpdata User.Branch User.Department --indent 4 > branch_department.json
#python manage.py dumpdata auth.user User.Branch User.Department User.UserProfile --indent 4 > users_backup05022026.json

#python manage.py dumpdata auth.user User.UserProfile > userbackup05052026.json
#python manage.py dumpdata User.Level > level_backup.json