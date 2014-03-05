import datetime
from tenancy.models import TenantModel
from django.db import models
from django.db.models import Sum, Q
from django.db.models.signals import post_save
from django.utils.timezone import now
from backapps.activity.models import Activity
from backapps.profile.models import Profile
from libs.chart.calculus import record2daily

class Record(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    Record is the most basic but important class. It stored the users activities.
    Each time the user click on a activity in the client app,
    a Record is created/updated.
    """
    #editable
    is_active      = models.BooleanField(default=True)
    activity       = models.ForeignKey(Activity)
    start_override = models.DateTimeField(blank=True, null=True)
    end_override   = models.DateTimeField(blank=True, null=True)
    #not editable
    user           = models.ForeignKey(Profile, editable=False)
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
    activity = models.ForeignKey(Activity, editable=False)
    user     = models.ForeignKey(Profile, editable=False)
    duration = models.DecimalField(default=0, max_digits=10, decimal_places=2, editable=False) # hours
    class Meta:
	unique_together = (("date", "activity", "user"),)

def update_DailyRecord(sender, instance, *args, **kwargs):
    workspace, activity, user = instance.tenant, instance.activity, instance.user
    if instance.start() and instance.end():
	start = instance.start().replace(hour=0, minute=0, second=0, microsecond=0)
	end = instance.end().replace(hour=0, minute=0, second=0, microsecond=0)
	end += datetime.timedelta(1)
	# get all records from the same period for the same activity & same user
	qs = Record.for_tenant(workspace).objects.filter(
		    ( Q(start_original__gte=start) & Q(start_override__isnull=True) ) | Q(start_override__gte=start)
		  , ( Q(end_original__lte=end) & Q(end_override__isnull=True) ) | Q(end_override__lte=end)
		  , activity=activity
		  , user=user
		  )
	# calculate
	data_dict = record2daily(qs)
	# update or create the daily_activity entries for the period and activity
	for date in data_dict.iterkeys():
	    (dpt, created) = DailyRecord.for_tenant(workspace
			      ).objects.get_or_create(
				activity=activity, date=date, user=user)
	    dpt.duration = data_dict[date].total_seconds()/3600
	    dpt.save()

post_save.connect(update_DailyRecord, sender=Record)

def get_ongoing_task(profile):
    """
    get the current "opened" (ongoing) record of the given user, if any
    """
    workspace = profile.tenant
    qs = Record.for_tenant(workspace).objects.filter(
				user=profile).order_by('start_original')
    ret = None
    if qs.count() > 0:
	last_record = qs[qs.count()-1]
	if last_record.end_original is None:
	    ret = last_record
    return ret
  
def new_task(profile, activity):
    """
    this is a safe function
    - close the current ongoing task, if any
    - create a new record, if a activity is given
    """
    workspace = profile.tenant
    #close last entry
    last_record = get_ongoing_task(profile)
    if last_record is not None:
	last_record.end_original = now()
	last_record.save()
    #create new entry
    cur_record = None
    if activity is not None:
	cur_record = Record.for_tenant(workspace).objects.create(
					      user=profile, activity=activity)
    return (last_record, cur_record)
