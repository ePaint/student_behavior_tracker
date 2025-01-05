from django.urls import path
from target_behaviors.views import Detail, Create, Edit
from target_behaviors.views import (
    delete_target_behavior,
    create_target_behavior_week,
    edit_target_behavior_week,
)

urlpatterns = [
    path("detail/<uuid:slug>/<uuid:user_uuid>/", Detail.as_view(), name=Detail.url_name),
    path("new/<uuid:user_uuid>/", Create.as_view(), name=Create.url_name),
    path("edit/<uuid:slug>/<uuid:user_uuid>/", Edit.as_view(), name=Edit.url_name),
    path("delete/<uuid:slug>/<uuid:user_uuid>/", delete_target_behavior, name='target-behaviors-delete'),
    path(
        "week/new/<uuid:slug>/<uuid:user_uuid>/",
        create_target_behavior_week,
        name="target-behaviors-week-create",
    ),
    path(
        "week/edit/<uuid:slug>/<uuid:user_uuid>/<uuid:week_uuid>/",
        edit_target_behavior_week,
        name="target-behaviors-week-edit",
    ),
]
