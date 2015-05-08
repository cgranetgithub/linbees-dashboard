from django.db import models
from libs.tenant import TenantModel
from django.utils.translation import ugettext_lazy as _

class PaymentData(TenantModel):
    '''
    Inherits TenantModel => tenant specific class
    '''
    key     = models.CharField(unique=True, max_length=255)
    value   = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
