from django.db import models
from libs.tenant import TenantModel
#from profile.models import Profile
#from task.models import Task
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class AutoRecord(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    Record is the most basic but important class as it stores the user
    activity. Each time the user clicks on a task in the client app,
    a Record is created and the previous "opened" one is closed.
    WARNING: start/date/task should never be modified after they have
    been set
    """
    is_active  = models.BooleanField(default=True)
    task       = models.ForeignKey('task.Task')
    start      = models.DateTimeField()
    end        = models.DateTimeField(blank=True, null=True)
    profile    = models.ForeignKey('profile.Profile')
    updated_at = models.DateTimeField(auto_now=True)
    user_agent = models.CharField(max_length=255)
    def __unicode__(self):
        return u'%s | %s | %s | %s'%(self.task, self.profile,
                                          self.start, self.end)
    def save(self, *args, **kw):
        if self.pk is not None:
            msg = u"Field %s changed in AutoRecord, that's forbiden"
            orig = AutoRecord.objects.get(pk=self.pk)
            if orig.start != self.start:
                raise ValidationError(msg%'start')
            if (orig.end is not None) and (orig.end != self.end):
                raise ValidationError(msg%'end')
            if orig.task != self.task:
                raise ValidationError(msg%'task')
        super(AutoRecord, self).save(*args, **kw)
        
class ManualRecord(TenantModel):
    """
    Used to manually declare or override record
    """
    is_active  = models.BooleanField(default=True)
    task       = models.ForeignKey('task.Task')
    start      = models.DateTimeField(blank=True, null=True)
    end        = models.DateTimeField(blank=True, null=True)
    profile    = models.ForeignKey('profile.Profile')
    updated_at = models.DateTimeField(auto_now=True)
    user_agent = models.CharField(max_length=255)
        
class DailyDataPerTaskPerUser(TenantModel):
    """
    duration & cost per day per task per user
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,
    by on_record_change, on post_save signal
    """
    date = models.DateField()
    task = models.ForeignKey('task.Task')
    wage = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    cost = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    profile = models.ForeignKey('profile.Profile')
    duration = models.DecimalField(default=0, max_digits=10,
                                                decimal_places=2) # hours
    time_ratio = models.DecimalField(default=0, max_digits=3,
                                                decimal_places=2)
    class Meta:
        unique_together = (("workspace", "date", "task", "profile"),)
    def __unicode__(self):
        return u'%s | %s | %s | %d | %d'%(self.date, self.task,
                                          self.profile, self.duration,
                                          self.cost)

class DailyDataPerTask(TenantModel):
    """
    duration & cost per day per task, including descendants
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,
    by on_record_change, on post_save signal
    """
    date = models.DateField()
    task = models.ForeignKey('task.Task')
    duration = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2) # hours
    cost     = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2)
    children_duration = models.DecimalField(default=0, max_digits=10,
                                            decimal_places=2)
    children_cost     = models.DecimalField(default=0, max_digits=10,
                                            decimal_places=2)
    class Meta:
        unique_together = (("workspace", "date", "task"),)
    def __unicode__(self):
        return u'%s | %s | %d | %d'%(self.date, self.task,
                                     self.duration, self.cost)

def get_ongoing_task(profile):
    """
    get the current "opened" (ongoing) record of the given user, if any
    """
    workspace = profile.workspace
    qs = AutoRecord.objects.filter(workspace=workspace,
                                   profile=profile).order_by('start')
    ret = None
    if qs.count() > 0:
        last_record = qs[qs.count()-1]
        if last_record.end is None:
            ret = last_record
    return ret

def new_task(profile, task):
    """
    this is a safe function
    - close the current ongoing task, if any
    - create a new record, if a task is given
    """
    workspace = profile.workspace
    #close last entry
    last_record = get_ongoing_task(profile)
    if last_record is not None:
        last_record.end = now()
        last_record.save()
    #create new entry
    cur_record = None
    if task is not None:
        cur_record = AutoRecord.objects.create(workspace=workspace,start=now(),
                                               profile=profile, task=task)
    return (last_record, cur_record)
