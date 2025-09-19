from django.contrib import admin
from django.urls import path
from app.views import symptom_input, register, user_login, ai_treatment, trend_data, charts, get_df, upload_view, upload_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", symptom_input, name = "symptom_input"),
    path("register/", register, name = "register"),
    path("login/",user_login, name = "login"),
    path("ai_treatment/", ai_treatment, name="ai_treatment"),
    path("trend_data/", trend_data, name="trend_data"),
    path("charts/", charts, name="charts"),
    path("get_df/", get_df, name="get_df"),
    path('upload_view/', upload_view, name='upload_view'),
    path("upload_data/", upload_data, name="upload_data"),
    
]
