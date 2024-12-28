from django.urls import path
from target_behaviors.views import Detail
from target_behaviors.views import (
    create_target_behavior_week,
    edit_target_behavior_week,
)

urlpatterns = [
    path("detail/<uuid:slug>/", Detail.as_view(), name=Detail.url_name),
    path(
        "week/new/",
        create_target_behavior_week,
        name="target-behaviors-week-create",
    ),
    path(
        "week/<uuid:slug>/",
        edit_target_behavior_week,
        name="target-behaviors-week-edit",
    ),
]
