from django.db import models
from django.conf import settings
from libs.tenant import TenantModel
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _

class Profile(MPTTModel, TenantModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                      primary_key=True)
    title = models.CharField(max_length=255, blank=True,
                             verbose_name=_('Title'))
    parent = TreeForeignKey('self', blank=True, null=True,
                            verbose_name=_('Manager'),
                            related_name='children')
    department = models.ForeignKey('department.Department',
                                   blank=True, null=True)
    has_accepted_terms = models.BooleanField(default=False,
                                             verbose_name=_('Accepted terms'))
    has_dashboard_access = models.BooleanField(
                                        default=False,
                                        verbose_name=_('Dashboard access'),
                                        help_text=_(
'''Authorize the user to access the dashboard. The user will only see ''' 
'''his own projects, the members of his teams and their projects.'''))
    is_hr = models.BooleanField(default=False,
                                verbose_name=_('Users information access'),
                                help_text=_(
'''Authorize the user to see and modify users information (name, tile, salary, activity). '''
'''But only for the members of his teams.'''))
    is_primary   = models.BooleanField(default=False,
                                       verbose_name=_('Projects full access'),
                                       help_text=_(
'''Authorize the user to see and modify all projects and create root (primary) projects.'''))
    power_transfer = models.ManyToManyField('self', blank=True,
                                            verbose_name=_(
'''has power transfer from'''))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('updated at'))
    @property
    def name(self):
        return self.user.get_full_name()
    #class MPTTMeta:
        #order_insertion_by = ['user']    
    def __unicode__(self):
        return '%s (%s)'%(self.name, self.user.email)

def createUserProfile(newuser, workspace):
    newuser.is_active = True
    newuser.save()
    profile = Profile.objects.create(workspace=workspace, user=newuser)
    return profile
