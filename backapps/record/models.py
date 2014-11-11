import datetime
from django.db import models
from django.db.models import Sum, Q
from django.db.models.signals import post_save
from django.utils.timezone import now
from backapps.profile.models import Profile
from backapps.task.models import Task
from libs.chart.calculus import record2daily
from libs.tenant import TenantModel

class Record(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    Record is the most basic but important class. It stored the users tasks.
    Each time the user click on a task in the client app,
    a Record is created/updated.
    """
    #editable
    is_active      = models.BooleanField(default=True)
    task       = models.ForeignKey(Task)
    start_override = models.DateTimeField(blank=True, null=True)
    end_override   = models.DateTimeField(blank=True, null=True)
    #not editable
    profile        = models.ForeignKey(Profile, editable=False)
    updated_at     = models.DateTimeField(auto_now=True)
    start_original = models.DateTimeField(auto_now_add=True)
    end_original   = models.DateTimeField(blank=True, null=True, editable=False)
    client         = models.CharField(max_length=255, editable=False)
    def start(self):
        """ returns if start_override datetime if it exists,
        otherise the start_original datetime.
        Result will never be None"""
        return self.start_override or self.start_original
    def end(self):
        """ returns if end_override datetime if it exists,
        otherise the end_original datetime, which can be null"""
        return self.end_override or self.end_original
        
class DailyRecord(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,\
    by update_DailyRecord, on post_save signal
    """
    date     = models.DateField(editable=False)
    task = models.ForeignKey(Task, editable=False)
    profile     = models.ForeignKey(Profile, editable=False)
    duration = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2, editable=False) # hours
    class Meta:
        unique_together = (("workspace", "date", "task", "profile"),)

def update_DailyRecord(sender, instance, *args, **kwargs):
    (workspace, task, profile) = (instance.workspace, instance.task,
                                  instance.profile)
    if instance.start() and instance.end():
        start = instance.start().replace(hour=0, minute=0,
                                         second=0, microsecond=0)
        end = instance.end().replace(hour=0, minute=0, second=0, microsecond=0)
        end += datetime.timedelta(1)
        # get all records from the same period for the same task & same user
        qs = Record.objects.by_workspace(workspace).filter(
                     (  Q(start_original__gte=start) 
                      & Q(start_override__isnull=True) )
                    | Q(start_override__gte=start)
                   , (  Q(end_original__lte=end) 
                      & Q(end_override__isnull=True) )
                    | Q(end_override__lte=end)
                   , task=task
                   , profile=profile
                )
        # calculate
        data_dict = record2daily(qs)
        # update or create the daily_task entries for the period and task
        for date in data_dict.iterkeys():
            (dpt, created) = DailyRecord.objects.get_or_create(
                                workspace=workspace,
                                task=task, date=date, profile=profile)
            dpt.duration = data_dict[date].total_seconds()/3600
            dpt.save()

post_save.connect(update_DailyRecord, sender=Record)

def get_ongoing_task(profile):
    """
    get the current "opened" (ongoing) record of the given user, if any
    """
    workspace = profile.workspace
    qs = Record.objects.by_workspace(workspace).filter(
                                profile=profile).order_by('start_original')
    ret = None
    if qs.count() > 0:
        last_record = qs[qs.count()-1]
        if last_record.end_original is None:
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
        last_record.end_original = now()
        last_record.save()
    #create new entry
    cur_record = None
    if task is not None:
        cur_record = Record.objects.create(workspace=workspace,
                                           profile=profile, task=task)
    return (last_record, cur_record)
