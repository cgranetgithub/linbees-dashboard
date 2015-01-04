import datetime
from django.db import models
from libs.tenant import TenantModel
from libs.chart.calculus import record2daily
from django.db.models.signals import post_save
from backapps.profile.models import Profile
from backapps.salary.models import DailySalary
from backapps.task.models import Task
from django.utils.timezone import now
from django.db.models import Sum, Q

class Record(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    Record is the most basic but important class. It stored the users tasks.
    Each time the user click on a task in the client app,
    a Record is created/updated.
    """
    #editable
    is_active      = models.BooleanField(default=True)
    task            = models.ForeignKey(Task)
    start_override = models.DateTimeField(blank=True, null=True)
    end_override   = models.DateTimeField(blank=True, null=True)
    #not editable
    profile        = models.ForeignKey(Profile)
    updated_at     = models.DateTimeField(auto_now=True)
    start_original = models.DateTimeField(auto_now_add=True)
    end_original   = models.DateTimeField(blank=True, null=True)
    client         = models.CharField(max_length=255)
    def start(self):
        """ returns if start_override datetime if it exists,
        otherise the start_original datetime.
        Result will never be None"""
        return self.start_override or self.start_original
    def end(self):
        """ returns if end_override datetime if it exists,
        otherise the end_original datetime, which can be null"""
        return self.end_override or self.end_original
        
class DailyDurationPerTaskPerUser(TenantModel):
    """
    duration per day per task per user
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,\
    by update_DailyDurationPerTaskPerUser, on post_save signal
    """
    date     = models.DateField()
    task     = models.ForeignKey(Task)
    profile  = models.ForeignKey(Profile)
    duration = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2) # hours
    class Meta:
        unique_together = (("workspace", "date", "task", "profile"),)
    def __unicode__(self):
        return u'%s | %s | %s | %s'%(self.profile, self.task, self.date,
                                     self.duration)

class DailyCostPerTaskPerUser(TenantModel):
    """
    cost per day per task per user
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,\
    by update_DailyCostPerTaskPerUser, on post_save signal
    """
    ddtu  = models.OneToOneField(DailyDurationPerTaskPerUser)
    time_percent = models.DecimalField(default=0, max_digits=3,
                                       decimal_places=2)
    wage     = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2)
    cost     = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2)
    class Meta:
        unique_together = (("workspace", "ddtu"),)
    def __unicode__(self):
        return u'%s | %s | %s | %s'%(self.ddtu.profile, self.ddtu.task,
                                     self.ddtu.date, self.cost)

class DailyDurationPerTask(TenantModel):
    """
    duration per day per task
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,\
    by update_DailyDurationPerTask, on post_save signal
    """
    date     = models.DateField()
    task     = models.ForeignKey(Task)
    duration = models.DecimalField(default=0, max_digits=10,
                                   decimal_places=2) # hours
    class Meta:
        unique_together = (("workspace", "date", "task"),)
    def __unicode__(self):
        return u'%s | %s | %s'%(self.task, self.date, self.duration)

class DailyCostPerTask(TenantModel):
    """
    cost per day per task
    Inherits TenantModel => tenant specific class
    automatically created/updated when Record changes,\
    by update_DailyCostPerTask, on post_save signal
    """
    date     = models.DateField()
    task     = models.ForeignKey(Task)
    cost = models.DecimalField(default=0, max_digits=10,
                               decimal_places=2)
    class Meta:
        unique_together = (("workspace", "date", "task"),)
    def __unicode__(self):
        return u'%s | %s | %s'%(self.task, self.date, self.cost)


def update_DailyDurationPerTaskPerUser(sender, instance, *args, **kwargs):
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
            (dpt, created) = DailyDurationPerTaskPerUser.objects.get_or_create(
                                workspace=workspace,
                                task=task, date=date, profile=profile)
            dpt.duration = data_dict[date].total_seconds()/3600
            dpt.save()

post_save.connect(update_DailyDurationPerTaskPerUser, sender=Record)

def update_DailyCostPerTaskPerUser(sender, instance, created, *args, **kwargs):
    workspace = instance.workspace
    profile   = instance.profile
    if sender == DailyDurationPerTaskPerUser:
        if created:
            DailyCostPerTaskPerUser.objects.create(workspace=workspace,
                                                   ddtu=instance)
        date = instance.date
        daily_tasks = DailyDurationPerTaskPerUser.objects.by_workspace(
                            workspace).filter(profile=profile, date=date)
        duration_sum = daily_tasks.aggregate(Sum('duration'))['duration__sum']
        if duration_sum != 0:
            daily_wage = 0
            try:
                daily_wage = DailySalary.objects.by_workspace(workspace).get(
                                    profile=profile,
                                    start_date__lte=date, end_date__gte=date
                                    ).daily_wage
            except DailySalary.DoesNotExist:
                pass
            ### !!! except more than one
                ### mistake somewhere
            for i in daily_tasks:
                dctu = i.dailycostpertaskperuser
                dctu.time_percent = i.duration / duration_sum
                dctu.wage = daily_wage
                dctu.cost = dctu.time_percent * dctu.wage
                dctu.save()
    elif sender == DailySalary:
        start_date = instance.start_date
        end_date   = instance.end_date
        new_wage   = instance.daily_wage
        daily_tasks = DailyDurationPerTaskPerUser.objects.by_workspace(
                            workspace).filter(profile=profile,
                                              date__gte=start_date,
                                              date__lte=end_date)
        for i in daily_tasks:
            dctu = i.dailycostpertaskperuser
            dctu.wage = new_wage
            dctu.cost = dctu.time_percent * dctu.wage
            dctu.save()

post_save.connect(update_DailyCostPerTaskPerUser,
                  sender=DailyDurationPerTaskPerUser)
post_save.connect(update_DailyCostPerTaskPerUser,
                  sender=DailySalary)

def update_DailyDurationPerTask(sender, instance, *args, **kwargs):
    workspace = instance.workspace
    task      = instance.task
    date      = instance.date
    duration_sum = DailyDurationPerTaskPerUser.objects.filter(
                            task=task, date=date
                            ).aggregate(Sum('duration'))['duration__sum']
    (ddt, created) = DailyDurationPerTask.objects.get_or_create(
                                workspace=workspace,
                                task=task, date=date)
    ddt.duration = duration_sum
    ddt.save()

post_save.connect(update_DailyDurationPerTask,
                  sender=DailyDurationPerTaskPerUser)

def update_DailyCostPerTask(sender, instance, *args, **kwargs):
    workspace = instance.workspace
    task      = instance.ddtu.task
    date      = instance.ddtu.date
    cost_sum = DailyCostPerTaskPerUser.objects.filter(
                            ddtu__task=task, ddtu__date=date
                            ).aggregate(Sum('cost'))['cost__sum']
    (dct, created) = DailyCostPerTask.objects.get_or_create(
                                workspace=workspace,
                                task=task, date=date)
    dct.cost = cost_sum
    dct.save()

post_save.connect(update_DailyCostPerTask,
                  sender=DailyCostPerTaskPerUser)


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
