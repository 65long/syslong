from django.contrib import admin
from .models import UserProfile, Role, WebRes
from .models import Organization, Department
# Register your models here.

admin.site.register([UserProfile, Role, WebRes, Organization, Department])
