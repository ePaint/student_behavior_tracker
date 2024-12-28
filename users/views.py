from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from users.forms import SignUpForm, ProfileEditForm


class SignIn(LoginView):
    template_name = 'users/signin.html'
    redirect_authenticated_user = True
    url_name = 'users-signin'


class SignUp(CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users-signin')
    form_class = SignUpForm
    url_name = 'users-signup'


class SignOut(LogoutView):
    url_name = 'users-signout'
    success_url = reverse_lazy('users-signin')


class Profile(DetailView):
    template_name = 'users/profile.html'
    url_name = 'users-profile'
    model = 'users.CustomUser'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileEdit(UpdateView):
    template_name = 'users/profile_edit.html'
    url_name = 'users-profile-edit'
    model = 'users.CustomUser'
    form_class = ProfileEditForm
    success_url = reverse_lazy('users-profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordUpdate(PasswordChangeView):
    template_name = 'users/password_update.html'
    url_name = 'users-password-update'
    success_url = reverse_lazy('users-profile-edit')
