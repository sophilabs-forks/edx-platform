"""
Admin site bindings for salesforce_registration
"""

from django.contrib import admin

# from config_models.admin import ConfigurationModelAdmin
from .models import SalesforceDomainEntry

class SalesforceDomainEntryAdmin(admin.ModelAdmin):
    list_display = ('domain', 'category')
    search_fields = ('domain', 'category')

admin.site.register(SalesforceDomainEntry, SalesforceDomainEntryAdmin)
