from django.db import models
from django.utils.translation import ugettext_lazy as _
from libs.tenant import TenantModel

class DailySalary(TenantModel):
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
    profile     = models.ForeignKey('profile.Profile',
                                    verbose_name=_('User'))
    start_date  = models.DateField(verbose_name=_('Start date'))
    end_date    = models.DateField(verbose_name=_('End date'))
    daily_wage  = models.DecimalField(default=0,
                                      max_digits=8, decimal_places=2,
                                      verbose_name=_('Daily wage'),
                                      help_text=_("This represents the "
"cost of the employee per day"))
    def __unicode__(self):
        return u'%s %s %s %s'%(self.profile, self.daily_wage,
                               self.start_date, self.end_date)