from django.contrib import admin

# Register your models here.
from . models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display=('email','username','company_name','date_joined','last_login','is_admin','is_staff')
    search_fields=('email','company_name') 
    readonly_fields=('date_joined','last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()
    ordering=('email',)

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email','username','company_name','phone','password1','password2'),
        }),
    )

admin.site.register(User,UserAdmin)