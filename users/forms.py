from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelChoiceField, CharField, PasswordInput, Form

from users.models import CustomUser


class SignUpForm(UserCreationForm):
    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(level_of_access_granted='Teacher')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'level_of_access_wanted', 'teacher', 'password1', 'password2']


class ProfileEditForm(UserChangeForm):
    password = None

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(level_of_access_granted='Teacher')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'level_of_access_wanted', 'teacher']
        exclude = ['password']


class AdminPasswordUpdateForm(Form):
    user = ModelChoiceField(queryset=CustomUser.objects.all())
    password1 = CharField(widget=PasswordInput, label='New Password')
    password2 = CharField(widget=PasswordInput, label='Confirm New Password')
