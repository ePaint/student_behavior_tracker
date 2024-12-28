from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'level_of_access_wanted', 'password1', 'password2']


class ProfileEditForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'level_of_access_wanted']
        exclude = ['password']
