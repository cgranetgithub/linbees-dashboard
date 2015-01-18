from django.db import models
from django.utils.translation import ugettext_lazy as _
from libs.tenant import TenantModel
from backapps.profile.models import Profile

class DailySalary(TenantModel):
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
    profile     = models.ForeignKey(Profile,
                                    verbose_name=_('user'))
    start_date  = models.DateField(verbose_name=_('start date'))
    end_date    = models.DateField(verbose_name=_('end date'))
    daily_wage  = models.DecimalField(default=0,
                                      max_digits=8, decimal_places=2,
                                      verbose_name=_('daily wage'),
                                      help_text=_("this represents the "
"cost of the employee per day"))
    def __unicode__(self):
        return u'%s %s %s %s'%(self.profile, self.daily_wage,
                               self.start_date, self.end_date)