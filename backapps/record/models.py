from django.db import models
from libs.tenant import TenantModel
from backapps.profile.models import Profile
from backapps.task.models import Task
from django.utils.timezone import now

#record_closed = django.dispatch.Signal(providing_args=["duration",])

class Record(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    Record is the most basic but important class as it stores the user
    activity. Each time the user clicks on a task in the client app,
    a Record is created and the previous "opened" one is closed.
    WARNING: start/date/task should never be modified after they have
    been set
    """
    is_active  = models.BooleanField(default=True)
    task       = models.ForeignKey(Task)
    start      = models.DateTimeField(blank=True, null=True)
    end        = models.DateTimeField(blank=True, null=True)
    profile    = models.ForeignKey(Profile)
    updated_at = models.DateTimeField(auto_now=True)
    user_agent = models.CharField(max_length=255)

    #def save(self, *args, **kwargs):
        #print self.start, self.end, self.task
        #super(Record, self).save(*args, **kwargs)

    #def set_end(self, value):
        #self.end = value
        #record_closed.send(sender=self.__class__,
                           #duration=end-start)
        
class DailyDataPerTaskPerUser(TenantModel):
    """
    duration&cost per day per task per user
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,
    by update_DailyDurationPerTaskPerUser, on post_save signal
    """
    date     = models.DateField()
    task     = models.ForeignKey(Task)
    profile  = models.ForeignKey(Profile)
    duration = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2) # hours
    ratio    = models.DecimalField(default=0, max_digits=3,
                                       decimal_places=2)
    wage     = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2)
    cost     = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2)
    class Meta:
        unique_together = (("workspace", "date", "task", "profile"),)
    def __unicode__(self):
        return u'%s | %s | %s | %s | %s'%(self.date, self.task,
                                          self.profile, self.duration,
                                          self.cost)

class DailyDataPerTask(TenantModel):
    """
    duration&cost per day per task, including descendants
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,
    by on_record_change, on post_save signal
    """
    date     = models.DateField()
    task     = models.ForeignKey(Task)
    duration = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2) # hours
    cost     = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2)
    class Meta:
        unique_together = (("workspace", "date", "task"),)
    def __unicode__(self):
        return u'%s | %s | %s | %s | %s'%(self.date, self.task,
                                          self.duration, self.cost)

#class DailyDurationPerTaskPerUser(TenantModel):
    #"""
    #duration per day per task per user
    #Inherits TenantModel => tenant specific class
    #automatically created/updated when Record changes,
    #by update_DailyDurationPerTaskPerUser, on post_save signal
    #"""
    #date     = models.DateField()
    #task     = models.ForeignKey(Task)
    #profile  = models.ForeignKey(Profile)
    #duration = models.DecimalField(default=0, max_digits=10,
                                   #decimal_places=2) # hours
    #class Meta:
        #unique_together = (("workspace", "date", "task", "profile"),)
    #def __unicode__(self):
        #return u'%s | %s | %s | %s'%(self.profile, self.task, self.date,
                                     #self.duration)

#class DailyCostPerTaskPerUser(TenantModel):
    #"""
    #cost per day per task per user
    #Inherits TenantModel => tenant specific class
    #automatically created/updated when DailyDurationPerTaskPerUser or
    #DailySalary change, by update_DailyCostPerTaskPerUser, 
    #on post_save signal
    #"""
    #ddtu  = models.OneToOneField(DailyDurationPerTaskPerUser)
    #time_percent = models.DecimalField(default=0, max_digits=3,
                                       #decimal_places=2)
    #wage     = models.DecimalField(default=0, max_digits=10,
                                   #decimal_places=2)
    #cost     = models.DecimalField(default=0, max_digits=10,
                                   #decimal_places=2)
    #class Meta:
        #unique_together = (("workspace", "ddtu"),)
    #def __unicode__(self):
        #return u'%s | %s | %s | %s'%(self.ddtu.profile, self.ddtu.task,
                                     #self.ddtu.date, self.cost)

#class DailyDurationPerTask(TenantModel):
    #"""
    #duration per day per task
    #Inherits TenantModel => tenant specific class
    #automatically created/updated when DailyDurationPerTaskPerUser changes,
    #by update_DailyDurationPerTask, on post_save signal
    #"""
    #date     = models.DateField()
    #task     = models.ForeignKey(Task)
    #duration = models.DecimalField(default=0, max_digits=10,
                                   #decimal_places=2) # hours
    #class Meta:
        #unique_together = (("workspace", "date", "task"),)
    #def __unicode__(self):
        #return u'%s | %s | %s'%(self.task, self.date, self.duration)

#class DailyCostPerTask(TenantModel):
    #"""
    #cost per day per task
    #Inherits TenantModel => tenant specific class
    #automatically created/updated when DailyCostPerTaskPerUser changes,
    #by update_DailyCostPerTask, on post_save signal
    #"""
    #date = models.DateField()
    #task = models.ForeignKey(Task)
    #cost = models.DecimalField(default=0, max_digits=10,
                               #decimal_places=2)
    #class Meta:
        #unique_together = (("workspace", "date", "task"),)
    #def __unicode__(self):
        #return u'%s | %s | %s'%(self.task, self.date, self.cost)

#class DailyCostPerHierarchy(TenantModel):
    #"""
    #cost per day per task, including its sub-tasks
    #Inherits TenantModel => tenant specific class
    #automatically created/updated when DailyCostPerTask changes,\
    #by update_DailyCostPerHierarchy, on post_save signal
    #"""
    #date = models.DateField()
    #task = models.ForeignKey(Task)
    #cost = models.DecimalField(default=0, max_digits=10,
                                   #decimal_places=2)
    #class Meta:
        #unique_together = (("workspace", "date", "task"),)
    #def __unicode__(self):
        #return u'%s | %s | %s'%(self.task, self.date, self.cost)

def get_ongoing_task(profile):
    """
    get the current "opened" (ongoing) record of the given user, if any
    """
    workspace = profile.workspace
    qs = Record.objects.by_workspace(workspace).filter(
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
        cur_record = Record.objects.create(workspace=workspace,
                                           profile=profile, task=task)
    return (last_record, cur_record)
