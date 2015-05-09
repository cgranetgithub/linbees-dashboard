import datetime
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_slug
import re

class Workspace(models.Model):
    """
    The workspace is the representation of the customer (company or organization).
    It is also the representation of a tenant in the multi-tenancy architecture\
    (tenant-specific models refer a a tenant model).
    Workspace contains mostly the organization information, especially information\
    required to issuing invoices.
    """
    #editable
    on_trial      = models.BooleanField(default=False,
                                        verbose_name=_("Trial mode"),
                                        help_text=_(
"""This field indicate that your are using your workspace for evaluation. Deactivate it once you are ready to go to production mode."""))
    contact_name  = models.CharField(max_length=255, blank=True,
                                    verbose_name=_('Main contact name'))
    contact_email = models.EmailField(max_length=255, blank=True,
                                    verbose_name=_('Main contact email'),
                                    help_text=_(
"""Will be used to send out important message (for instance invoices)"""))
    address1      = models.CharField(max_length=255, blank=True,
                                    verbose_name=_("Address (line1)"))
    address2      = models.CharField(max_length=255, blank=True)
    zipcode       = models.IntegerField(blank=True, null=True,
                                        verbose_name=_('Zipcode'))
    city          = models.CharField(max_length=255, blank=True,
                                    verbose_name=_('City'))
    country       = models.CharField(max_length=255, blank=True,
                                    verbose_name=_('Country'))
    phone_number  = models.CharField(max_length=255, blank=True,
                                    verbose_name=_('Phone number'))
    #not editable
    is_active   = models.BooleanField(default=True, editable=False,
                                    verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                    verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                    verbose_name=_('updated at'))
    name        = models.SlugField(unique=True, editable=False,
                                verbose_name=_('Dashboard name'),
                                help_text=_(
"""By default, the dashboard name is your company email domain"""))
    paid_until  = models.DateField(null=True
                                    , editable=False
                                    , verbose_name=_('Next invoice date')
                                    , help_text=_(
"""Date until when the oranization has paid its subscription. At creation time, paid_until is initiaized with now + the default trial period defined in the settings."""))
    monthly_user_fee = models.DecimalField(max_digits=5
                                    , decimal_places=2
                                    , default=0
                                    , editable=False
                                    , verbose_name=_('Monthly user fee')
                                    , help_text=_(
"""Monthly rate applied to calculate the monthly fee. Monthly fee is number of active users x rate."""))
    monthly_fixed_fee = models.DecimalField(max_digits=7
                                    , decimal_places=2
                                    , default=0
                                    , editable=False
                                    , verbose_name=_('Monthly fixed fee')
                                    , help_text=_(
"""Fee per month, independent of the number of users"""))
    yearly_fixed_fee = models.DecimalField(max_digits=8
                                    , decimal_places=2
                                    , default=0
                                    , editable=False
                                    , verbose_name=_('Yearly fixed fee')
                                    , help_text=_(
"""Fee per year, independent of the number of users"""))
    def __unicode__(self):
        """ used in the admin """
        return u'%s'%self.name
    def company_name(self):
        return self.name.split('-')[0]

def getDashboardNameFromEmail(email):
    #return email.split('@')[1].replace('.', '-')
    return email.split('@')[1]
