from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)
admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(MainGroup)
#admin.site.register(GroupEmail)
admin.site.register(GroupUser)
