from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from model_utils import Choices
from model_utils.fields import UUIDField
from users.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = UUIDField(version=4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    LEVELS_OF_ACCESS = Choices('Student', 'Teacher', 'Admin')
    level_of_access_wanted = models.CharField(choices=LEVELS_OF_ACCESS, default=LEVELS_OF_ACCESS.Student, max_length=10)
    level_of_access_granted = models.CharField(choices=LEVELS_OF_ACCESS, default=LEVELS_OF_ACCESS.Student, max_length=10)
    teacher = models.ForeignKey('self', on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    target_behaviors = models.ManyToManyField('target_behaviors.TargetBehavior', related_name='users', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.email
