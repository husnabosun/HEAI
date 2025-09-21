from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SymptomRecord , VoiceRecord, MyUser

@admin.register(SymptomRecord)
class SymptomRecordAdmin(admin.ModelAdmin):
    list_display = ("disease", "branch", "created_at") 


@admin.register(VoiceRecord)
class VoiceRecordAdmin(admin.ModelAdmin):
    list_display = ("audio_file", "summary", "created_at") 
    
class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ("tc", "is_admin", "is_active")
    list_filter = ("is_admin", "is_active")
    fieldsets = (
        (None, {"fields": ("tc", "password")}),
        ("Yetkiler", {"fields": ("is_admin", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("tc", "password1", "password2", "is_active", "is_admin", "is_superuser"),
        }),
    )
    search_fields = ("tc",)
    ordering = ("tc",)

admin.site.register(MyUser, MyUserAdmin)
