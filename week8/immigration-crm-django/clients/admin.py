from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'full_name', 'visa_type', 'current_status', 'filing_date', 'created_at']
    list_filter = ['visa_type', 'current_status', 'country_of_origin']
    search_fields = ['first_name', 'last_name', 'case_number', 'email']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
