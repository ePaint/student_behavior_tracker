from django.urls import path, re_path
from django.views.generic import RedirectView
from layout.views import Home

favicon_view = RedirectView.as_view(url="/static/layout/favicon.png", permanent=True)

urlpatterns = [
    path("", Home.as_view(), name=Home.url_name),
    re_path(r"^favicon\.ico$", favicon_view),
]
