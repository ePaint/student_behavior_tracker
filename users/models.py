from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from users.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    target_behaviors = models.ManyToManyField('target_behaviors.TargetBehavior', related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.email
