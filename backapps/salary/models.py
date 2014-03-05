from django.db import models
from django.utils.translation import ugettext_lazy as _
from tenancy.models import TenantModel
from backapps.profile.models import Profile

class FixedSalary(TenantModel):
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    user        = models.ForeignKey(Profile, editable=False
					, verbose_name=_('user'))
    start_date  = models.DateField(verbose_name=_('start date'))
    end_date    = models.DateField(verbose_name=_('end date'))
    monthly_wage  = models.DecimalField(max_digits=8, decimal_places=2
					, verbose_name=_('monthly wage')
					, help_text=_("this reprensents the "
"cost of the employee per month"))
