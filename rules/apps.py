# Django Built-in Modules
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class RulesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rules'

    verbose_name = _("قوانین و مقررات")
