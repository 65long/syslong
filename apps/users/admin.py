from django.contrib import admin
from .models import UserProfile, Role, WebResource
from .models import Organization
# Register your models here.

admin.site.register([UserProfile, Role, WebResource, Organization])
