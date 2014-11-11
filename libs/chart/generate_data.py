import random, datetime, math
from django.utils.timezone import utc
from django.contrib.auth.models import User
from backapps.record.models import Record, DailyRecord
from backapps.task.models import Task
from backapps.profile.models import Profile, createUserProfile

def fn(x, length):
    return 3.0*math.cos((x+length)/(length/3.0))+4.0

def clean_users(workspace, user):
    existing = Profile.objects.by_workspace(workspace).exclude(user=user)
    user_list = [i.user for i in existing]
    existing.delete()
    for i in user_list:
        i.delete()

def generate_users(workspace, nb=10):
    for i in range(nb):
        email = 'user%i@%s'%(i, workspace.name.replace('-', '.'))
        user = User.objects.create_user(username=email, password=email, email=email)
        createUserProfile(user, workspace)

def clean_tasks(workspace):
    existing = Task.objects.by_workspace(workspace).all()
    existing.delete()

def generate_tasks(workspace, user, nb=10):
    owner = Profile.objects.by_workspace(workspace).get(user=user)
    for n in range(nb):
        name = "Task_%d"%n
        Task.objects.create(workspace=workspace, name=name, owner=owner)

def clean_records(workspace):
    existing = DailyRecord.objects.by_workspace(workspace).all()
    existing.delete()
    existing = Record.objects.by_workspace(workspace).all()
    existing.delete()

def generate_records(workspace, begin_date=None, end_date=None):
    tasks = Task.objects.by_workspace(workspace).all()
    if tasks.count() < 1:
        return
    if end_date is None:
        end_date = datetime.datetime.today()
    if begin_date is None:
        begin_date = end_date - datetime.timedelta(10)
    nb_days = (end_date - begin_date).days
    users = Profile.objects.by_workspace(workspace).all()
    cur = begin_date
    dailyrecord_list = []
    for u in users:
        if tasks.count() > 5:
            nb = 5
        else:
            nb = tasks.count()
        working_on = random.randint(1, nb)
        plist = random.sample(tasks, working_on)
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
                Record.objects.create(workspace=workspace, user=u, task=p,
                                      start_override=start, end_original=end)
                d = (random.uniform(7, 8) - cum)/(working_on)
                cum +=d
            cur += datetime.timedelta(1)
            ite += 1
