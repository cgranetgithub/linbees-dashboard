from django.db import models
from libs.tenant import TenantModel
from mptt.models import MPTTModel, TreeForeignKey
#from profile.models import Profile
from django.utils.translation import ugettext_lazy as _
import django.dispatch

parent_changed = django.dispatch.Signal(providing_args=["previous", "new"])

class TaskGroup(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
    name        = models.CharField(unique=True, max_length=255,
                                   verbose_name=_('Name'))
    description = models.CharField(max_length=255, blank=True,
                                   verbose_name=_('Description'))

class TaskType(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
    name        = models.CharField(unique=True, max_length=255,
                                   verbose_name=_('Name'))
    description = models.CharField(max_length=255, blank=True,
                                   verbose_name=_('Description'))

class Task(MPTTModel, TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True,
                                      verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True,
                                       verbose_name=_('updated at'))
    monitored   = models.BooleanField(default=True,
                                      verbose_name=_('Monitored'))
    primary     = models.BooleanField(default=False,
                                      verbose_name=_('Primary'))
    personal    = models.BooleanField(default=False,
                                      verbose_name=_('Personal'))
    name        = models.CharField(max_length=255,
                                   verbose_name=_('Name'))
    description = models.CharField(max_length=255, blank=True,
                                   verbose_name=_('Description'))
    p_group     = models.ForeignKey(TaskGroup, blank=True, null=True,
                                    verbose_name=_('Group'))
    p_type      = models.ForeignKey(TaskType, blank=True, null=True,
                                    verbose_name=_('Type'))
    parent      = TreeForeignKey('self', blank=True, null=True,
                                 verbose_name=_('Parent project'),
                                 help_text=_('Parent project'),
                                 related_name='children_task')
    owner       = models.ForeignKey('profile.Profile',
                                    verbose_name=_('Owned by'))
    start_date  = models.DateField(blank=True, null=True,
                                   verbose_name=_('Start date (planned)'))
    end_date    = models.DateField(blank=True, null=True,
                                   verbose_name=_('End date (planned)'))
    additional_cost = models.IntegerField(blank=True, null=True,
                                    verbose_name=_('Additional cost'))
    cost_estimate = models.IntegerField(blank=True, null=True,
                                    verbose_name=_('Cost (planned)'))
    time_estimate = models.IntegerField(blank=True, null=True,
                                    verbose_name=_('Time (planned, in hours)'))
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = (('workspace', 'name', 'parent'),)
    #class MPTTMeta:
        #order_insertion_by = ['name']
    def __unicode__(self):
        if self.parent is not None:
            return u'%s/%s'%(self.parent, self.name)
        else:
            return u'%s'%(self.name)
    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Task.objects.get(pk=self.pk)
            if orig.parent != self.parent:
                parent_changed.send_robust(sender=self.__class__,
                                           instance=self,
                                           prev_parent=orig.parent,
                                           new_parent=self.parent)
        super(Task, self).save(*args, **kw)
