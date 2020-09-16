from django.contrib import admin
from .models import UserProfile, Leaves, Personal_info

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Leaves)
admin.site.register(Personal_info)
