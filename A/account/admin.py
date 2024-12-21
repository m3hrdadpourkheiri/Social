from django.contrib import admin
from .models import Relation,Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Relation)



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)

#admin.site.register(Profile)