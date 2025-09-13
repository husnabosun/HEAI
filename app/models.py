from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, tc, password=None):
        if not tc:
            raise ValueError("T.C kimlik numarası zorunludur.")
        user = self.model(tc=tc)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, tc, password=None, **extra_fields):
        if not tc:
            raise ValueError("Username field should be filled")
        user = self.model(tc=tc, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    tc = models.CharField(max_length=11, unique=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = "tc"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.tc 
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin