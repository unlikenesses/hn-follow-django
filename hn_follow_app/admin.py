from django.contrib import admin
from .models import HnUser, HnSubmission

admin.site.register(HnUser)
admin.site.register(HnSubmission)
