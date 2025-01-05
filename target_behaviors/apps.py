from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TargetBehaviorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'target_behaviors'
    verbose_name = _('goals')
