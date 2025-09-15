from django.contrib import admin

from .models import SymptomRecord

@admin.register(SymptomRecord)
class SymptomRecordAdmin(admin.ModelAdmin):
    list_display = ("disease", "branch", "created_at") 
