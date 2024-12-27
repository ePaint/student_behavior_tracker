from django.urls import path
from layout.views import Home

urlpatterns = [
    path('', Home.as_view(), name=Home.url_name),
]
