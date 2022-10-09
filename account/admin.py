from django.contrib import admin

from .models import User,Role,userProfile,userProfileDetail

# Register your models here.



class UserAdmin(admin.ModelAdmin):
    list_display = ( 'first_name','email','mobile')


admin.site.register(User)
admin.site.register(Role)
admin.site.register(userProfile)
admin.site.register(userProfileDetail)