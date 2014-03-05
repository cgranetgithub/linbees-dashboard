from django.db import models
from django.utils.translation import ugettext_lazy as _
from tenancy.models import TenantModel

class Invoice(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    sent_at     = models.DateTimeField(blank=True, null=True
					    , verbose_name=_('sent at'))
    month       = models.IntegerField(verbose_name=_('month'))
    year        = models.IntegerField(verbose_name=_('year'))
    amount      = models.IntegerField(verbose_name=_('amount'))
    comment     = models.CharField(max_length=255, blank=True
					    , verbose_name=_('comment'))
    pdf         = models.FileField(upload_to='invoices')
