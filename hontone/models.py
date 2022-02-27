from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db import models

class HontoneUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("Users must have a valid username")
        if not password:
            # TODO: Add validation for password here?
            raise ValueError("Users must have a valid password")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class HontoneUser(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = HontoneUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
