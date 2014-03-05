from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from tenancy.models import TenantModel
from backapps.profile.models import Profile

PREFERENCES_DICT = {
    'ClientAlwaysOnTop' : {'value' : 'True', 'text' : _('Keep on top')}, 
    }

class Preference(TenantModel):
    '''
    Inherits TenantModel => tenant specific class
    '''
    user  = models.ForeignKey(Profile, editable=False)
    key   = models.CharField(max_length=255, editable=False)
    value = models.CharField(max_length=255)
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    class Meta:
	unique_together = (('user', 'key'),)

def create_prefs(sender, instance, *args, **kwargs):
    workspace, user = instance.tenant, instance
    for (i,j) in PREFERENCES_DICT.iteritems():
	Preference.for_tenant(workspace).objects.get_or_create(
					    user=user, key=i, 
					    defaults = {'value':j['value']})

post_save.connect(create_prefs, sender=Profile)
