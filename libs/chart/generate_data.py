import math
import random, string, datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
from backapps.record.models import Record, DailyRecord
from backapps.activity.models import Activity
from backapps.profile.models import Profile, createUserProfile

def fn(x, length):
    return 3.0*math.cos((x+length)/(length/3.0))+4.0

def clean_users(workspace, user):
    existing = Profile.for_tenant(workspace).objects.exclude(user=user)
    existing.delete()
  
def generate_users(workspace, nb=10):
    for i in range(nb):
	email = 'user%i@%s'%(i, workspace.name.replace('-', '.'))
	user = User.objects.create_user(username=email, password=email, email=email)
	createUserProfile(user, workspace)

def clean_activities(workspace):
    existing = Activity.for_tenant(workspace).objects.all()
    existing.delete()

def generate_activities(workspace, nb=10):
    for n in range(nb):
    #activities = ["Moon", "Sand", "Ocean", "Fire", "Cloud", "Deep", "Car", "Earth"]
    #for p in activities:
	name = "Activity_%d"%n
	Activity.for_tenant(workspace).objects.create(name=name)

def clean_records(workspace):
    existing = DailyRecord.for_tenant(workspace).objects.all()
    existing.delete()
    existing = Record.for_tenant(workspace).objects.all()
    existing.delete()

def generate_records(workspace, begin_date=None, end_date=None):
    activities = Activity.for_tenant(workspace).objects.all()
    if activities.count() < 1:
	return
    if end_date is None:
	end_date = datetime.datetime.today()
    if begin_date is None:
	begin_date = end_date - datetime.timedelta(10)
    nb_days = (end_date - begin_date).days
    users = Profile.for_tenant(workspace).objects.all()
    cur = begin_date
    dailyrecord_list = []
    for u in users:
	if activities.count() > 5:
	    nb = 5
	else:
	    nb = activities.count()
	working_on = random.randint(1, nb)
	plist = random.sample(activities, working_on)
	cur = begin_date
	ite = random.randint(1, nb_days)
	while cur != end_date:
	    start = datetime.datetime(cur.year, cur.month, cur.day
						      , 9,  0, 0, tzinfo=utc)
	    d = fn(ite, nb_days)
	    cum = d
	    for p in plist:
		delta = datetime.timedelta(hours=int(d), minutes=int(d%1*60))
		end = start + delta
		Record.for_tenant(workspace).objects.create(user=u
							  , activity=p
							  , start_override=start
							  , end_original=end)
		d = (random.uniform(7, 8) - cum)/(working_on)
		cum +=d
	    cur += datetime.timedelta(1)
	    ite += 1
