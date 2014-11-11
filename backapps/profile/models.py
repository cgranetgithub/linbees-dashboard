from django.db import models
from libs.tenant import TenantModel
from django.utils.translation import ugettext_lazy as _
from backapps.department.models import Department ### TENANT CLASS
from django.contrib.auth.models import User

class Profile(TenantModel):
    user       = models.OneToOneField(User, primary_key=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    parent     = models.ForeignKey('self', blank=True, null=True,
                                   verbose_name=_('depends on'))
    has_accepted_terms = models.BooleanField(default=False,
                                             verbose_name=_('accepted terms'))
    is_active          = models.BooleanField(default=True,
                                             verbose_name=_('active'))
    is_admin_workspace = models.BooleanField(default=False,
                                             verbose_name=_('workspace admin'))
    is_admin_hr        = models.BooleanField(default=False,
                                             verbose_name=_('HR admin'))
    is_admin_primary   = models.BooleanField(default=False,
                                             verbose_name=_('primary '
'tasks admin'))
    power_transfer = models.ManyToManyField('self', blank=True,
                                            verbose_name=_('has power '
'transfer from'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('updated at'))
    def __unicode__(self):
        return u'%s'%self.user.email

def createUserProfile(newuser, workspace):
    newuser.is_active = True
    newuser.save()
    profile = Profile.objects.create(workspace=workspace, user=newuser)
    return profile
