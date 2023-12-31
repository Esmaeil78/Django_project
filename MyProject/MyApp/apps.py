from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MyApp'
    verbose_name = _('نرم افزار انبارداری')