from django.db import models
from django.utils.translation import ugettext_lazy as _
from libs.tenant import TenantModel

class Department(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
    name        = models.CharField(unique=True, max_length=255,
                                   verbose_name=_('Name'))
    description = models.CharField(max_length=255, blank=True,
                                   verbose_name=_('Description'))
