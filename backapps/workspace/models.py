from tenancy.models import AbstractTenant
from django.conf import settings
import datetime
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_slug
import re

class Workspace(AbstractTenant):
    """
    Inherits AbstractTenant (see django-tenancy module)
    The workspace is the representation of the customer (company or organization).
    It is also the representation of a tenant in the multi-tenancy architecture\
    (tenant-specific models refer a a tenant model).
    Workspace contains mostly the organization information, especially information\
    required to issuing invoices.
    """
    #editable
    on_trial      = models.BooleanField(default=False
				    , verbose_name=_("in trial mode")
				    , help_text=_("this field indicate that your "
"are using your workspace for evaluation. Deactivate it once you are ready to go "
"to production mode."))
    contact_name  = models.CharField(max_length=255, blank=True
				    , verbose_name=_('main contact name'))
    contact_email = models.EmailField(max_length=255, blank=True
				    , verbose_name=_('main contact email address')
				    , help_text=_("Will be used to send out "
"important message (for instance invoices)"))
    address1      = models.CharField(max_length=255, blank=True
				    , verbose_name=_("address (line1)"))
    address2      = models.CharField(max_length=255, blank=True)
    zipcode       = models.IntegerField(blank=True, null=True
				    , verbose_name=_('zipcode'))
    city          = models.CharField(max_length=255, blank=True
				    , verbose_name=_('city'))
    country       = models.CharField(max_length=255, blank=True
				    , verbose_name=_('country'))
    phone_number  = models.CharField(max_length=255, blank=True
				    , verbose_name=_('phone number'))
    #not editable
    is_active   = models.BooleanField(default=True, editable=False
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    name        = models.SlugField(unique=True, editable=False
				    , verbose_name=_('dashboard name')
				    , help_text=_("by default, the dashboard "
"name is your company email domain"))
    paid_until  = models.DateField(default=
				      now().date()
				    + datetime.timedelta(
						  settings.DEFAULT_FREE_PERIOD)
				    , editable=False
				    , verbose_name=_('next invoice date')
				    , help_text="date until when the oranization "
"has paid its subscription. At creation time, paid_until is initiaized with now "
"+ the default trial period defined in the settings.")
    monthly_user_fee = models.DecimalField(max_digits=5
				    , decimal_places=2
				    , default=settings.DEFAULT_PRICE
				    , editable=False
				    , verbose_name=('monthly user fee')
				    , help_text="monthly rate applied to "
"calculate the monthly fee. Monthly fee is number of active users x rate.")
    monthly_fixed_fee = models.DecimalField(max_digits=7
				    , decimal_places=2
				    , default=0
				    , editable=False
				    , verbose_name=('monthly fixed fee')
				    , help_text="fee per month, independent "
"of the number of users")
    yearly_fixed_fee = models.DecimalField(max_digits=8
				    , decimal_places=2
				    , default=0
				    , editable=False
				    , verbose_name=('yearly user fee')
				    , help_text="fee per year, independent "
"of the number of users")
    # DO NOT remove natural_key, this is required by django-tenancy
    def natural_key(self):
	return ((self.name, ))

def getDashboardNameFromEmail(email):
    return email.split('@')[1].replace('.', '-')
