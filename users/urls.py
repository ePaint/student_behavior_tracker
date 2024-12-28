from django.urls import path
from users.views import SignIn, SignUp, SignOut, Profile, ProfileEdit, PasswordUpdate

urlpatterns = [
    path('signin/', SignIn.as_view(), name=SignIn.url_name),
    path('signup/', SignUp.as_view(), name=SignUp.url_name),
    path('signout/', SignOut.as_view(), name=SignOut.url_name),
    path('profile/', Profile.as_view(), name=Profile.url_name),
    path('profile/edit/', ProfileEdit.as_view(), name=ProfileEdit.url_name),
    path('profile/password/', PasswordUpdate.as_view(), name=PasswordUpdate.url_name),
]
