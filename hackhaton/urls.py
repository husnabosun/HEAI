from django.contrib import admin
from django.urls import path
from app.views import symptom_input, register, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", symptom_input, name = "symptom_input"),
    path("register/", register, name = "register"),
    path("login/",user_login, name = "login")
]
