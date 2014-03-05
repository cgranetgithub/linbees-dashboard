from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tenancy.models import TenantModel
from backapps.department.models import Department
from backapps.workspace.models import Workspace

class TenantLink(models.Model):
    user      = models.OneToOneField(User, primary_key=True)
    workspace = models.ForeignKey(Workspace)
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))

class Profile(TenantModel):
    user       = models.OneToOneField(User, primary_key=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    parent     = models.ForeignKey('self', blank=True, null=True
					   , verbose_name=_('depends on'))
    has_accepted_terms = models.BooleanField(default=False
					   , verbose_name=_('accepted terms'))
    is_active          = models.BooleanField(default=True
					   , verbose_name=_('active'))
    is_admin_workspace = models.BooleanField(default=False
					   , verbose_name=_('workspace admin'))
    is_admin_hr        = models.BooleanField(default=False
					   , verbose_name=_('HR admin'))
    is_admin_primary   = models.BooleanField(default=False
					   , verbose_name=_('primary '
'activities admin'))
    power_transfer = models.ManyToManyField('self', blank=True
					   , verbose_name=_('has power '
'transfer from'))
    created_at = models.DateTimeField(auto_now_add=True
					   , verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True
					   , verbose_name=_('updated at'))
    def __unicode__(self):
        return u'%s'%self.user.email

def createUserProfile(newuser, workspace):
    newuser.is_active = True
    newuser.save()
    TenantLink.objects.create(user=newuser, workspace=workspace)
    profile = Profile.for_tenant(workspace).objects.create(user=newuser)
    return profile
