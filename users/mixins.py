from django.core.exceptions import PermissionDenied


class TeacherRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.level_of_access_granted in ['Teacher', 'Admin']:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
