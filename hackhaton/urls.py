from django.contrib import admin
from django.urls import path
from app.views import symptom_input, register, user_login, ai_treatment, trend_data, charts

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", symptom_input, name = "symptom_input"),
    path("register/", register, name = "register"),
    path("login/",user_login, name = "login"),
    path("ai_treatment/", ai_treatment, name="ai_treatment"),
    path("trend_data/", trend_data, name="trend_data"),
    path("charts/", charts, name="charts")
    
]
