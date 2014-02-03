from django.contrib import admin
from mentor.users.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # Thsi changes UserAdmin list form
    list_display = ('username','is_staff','is_mentor')

admin.site.register(User, UserAdmin)