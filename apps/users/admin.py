from django.contrib import admin
from .models import UserProfile, Role, WebRes
# Register your models here.

admin.site.register([UserProfile, Role, WebRes])
