from django.db import models
from django.utils.translation import ugettext_lazy as _
from tenancy.models import TenantModel
from backapps.profile.models import Profile

class TaskGroup(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    name        = models.CharField(unique=True, max_length=255
					      , verbose_name=_('name'))
    description = models.CharField(max_length=255, blank=True
					      , verbose_name=_('description'))

class TaskType(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    name        = models.CharField(unique=True, max_length=255
					    , verbose_name=_('name'))
    description = models.CharField(max_length=255, blank=True
					    , verbose_name=_('description'))

class Task(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    monitored   = models.BooleanField(default=True
					      , verbose_name=_('monitored'))
    primary     = models.BooleanField(default=False
					    , verbose_name=_('primary'))
    name        = models.CharField(max_length=255
					      , verbose_name=_('name'))
    description = models.CharField(max_length=255, blank=True
					      , verbose_name=_('description'))
    p_group     = models.ForeignKey(TaskGroup, blank=True, null=True
					      , verbose_name=_('group'))
    p_type      = models.ForeignKey(TaskType, blank=True, null=True
					      , verbose_name=_('type'))
    parent      = models.ForeignKey('self', blank=True, null=True
					      , verbose_name=_('sub-task of'))
    owner       = models.ForeignKey(Profile, verbose_name=_('owned by'))
    def __unicode__(self):
	ret = ""
	if self.parent:
	    ret = self.parent + "/"
	return u'%s%s'%(ret, self.name)
    class Meta:
	verbose_name = "Task"
	verbose_name_plural = "Tasks"
	unique_together = (('name', 'parent'),)
