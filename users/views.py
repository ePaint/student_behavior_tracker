from braces.views import SuperuserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from users.forms import SignUpForm, ProfileEditForm, AdminPasswordUpdateForm
from users.mixins import TeacherRequiredMixin
from users.models import CustomUser


class SignIn(LoginView):
    template_name = 'users/signin.html'
    url_name = 'users-signin'

    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('users-profile')


class SignUp(CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users-signin')
    form_class = SignUpForm
    url_name = 'users-signup'


class SignOut(LoginRequiredMixin, LogoutView):
    url_name = 'users-signout'
    success_url = reverse_lazy('users-signin')


class ProfileOther(LoginRequiredMixin, TeacherRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    url_name = 'users-profile-other'
    model = 'users.CustomUser'
    context_object_name = 'user'
    slug_field = "uuid"

    def get_object(self, queryset=None):
        return CustomUser.objects.get(uuid=self.kwargs.get('slug'))


class Profile(LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    url_name = 'users-profile'
    model = 'users.CustomUser'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileEdit(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile_edit.html'
    url_name = 'users-profile-edit'
    model = 'users.CustomUser'
    form_class = ProfileEditForm
    success_url = reverse_lazy('users-profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordUpdate(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_update.html'
    url_name = 'users-password-update'
    success_url = reverse_lazy('users-profile-edit')


#
class AdminPasswordUpdate(LoginRequiredMixin, SuperuserRequiredMixin, FormView):
    template_name = 'users/admin_password_update.html'
    url_name = 'users-admin-password-update'
    success_url = reverse_lazy('users-profile')
    form_class = AdminPasswordUpdateForm

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        user.set_password(form.cleaned_data.get('password1'))
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users-profile')
