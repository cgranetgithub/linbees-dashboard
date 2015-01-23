import random, datetime, math
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from backapps.profile.models import Profile, createUserProfile
from backapps.record.models import (AutoRecord, DailyDataPerTaskPerUser,
                                    DailyDataPerTask)
from backapps.salary.models import DailySalary
from backapps.task.models import Task

def fn(x, length):
    return 3.0*math.cos((x+length)/(length/3.0))+4.0

def clean_users(workspace, user):
    profiles = Profile.objects.exclude(user=user, workspace=workspace)
    user_list = [i.user for i in profiles]
    DailySalary.objects.filter(workspace=workspace).delete()
    profiles.delete()
    for i in user_list:
        i.delete()

def generate_users(workspace, start_date, end_date, nb=10):
    parent_ids = []
    extension = workspace.name.replace('-', '.')
    ceo_email = 'ceo@%s'%extension
    (ceo, created) = User.objects.get_or_create(username=ceo_email)
    ceo.email = ceo_email
    ceo.first_name = 'CEO'
    ceo.has_dashboard_access = True
    ceo.is_hr = True
    ceo.is_primary = True
    if created:
        ceo.password = make_password('test')
        createUserProfile(ceo, workspace)
    ceo.save()
    ceo.profile.has_dashboard_access = True
    ceo.profile.is_hr = True
    ceo.profile.is_primary = True
    ceo.profile.save()
    DailySalary.objects.create(workspace=workspace, profile=ceo.profile,
                               daily_wage=random.randint(1500, 2000),
                               start_date=start_date, end_date=end_date)
    for (i, j) in ( ('rd', 'R&D'),
                    ('marketing', 'Marketing'),
                    ('sales', 'Sales' ) ):
        user = User.objects.create_user(username='%s@%s'%(i, extension),
                                        password='test',
                                        email='%s@%s'%(i, extension),
                                        first_name=j)
        profile = createUserProfile(user, workspace)
        profile.parent = ceo.profile
        profile.save()
        parent_ids.append(user.id)
        DailySalary.objects.create(workspace=workspace, profile=profile,
                                   daily_wage=random.randint(900, 1500),
                                   start_date=start_date, end_date=end_date)
    if nb > 4:
        for i in range(nb-4):
            email = 'user%i@%s'%(i, extension)
            user = User.objects.create_user(username=email, password='test',
                                            email=email, first_name='user%i'%(i))
            profile = createUserProfile(user, workspace)
            profile.parent = Profile.objects.get(
                                        user__id=random.choice(parent_ids))
            profile.save()
            parent_ids.append(user.id)
            DailySalary.objects.create(workspace=workspace, profile=profile,
                                    daily_wage=random.randint(500, 1000),
                                    start_date=start_date, end_date=end_date)

def clean_tasks(workspace):
    existing = Task.objects.filter(workspace=workspace)
    existing.delete()

def generate_tasks(workspace, user, nb=10):
    task_nb = 0
    task_ids = []
    n = 1
    extension = workspace.name.replace('-', '.')
    ceo = Profile.objects.get(workspace=workspace, 
                                        user__username='ceo@%s'%extension)
    rd = Profile.objects.get(workspace=workspace, 
                                        user__username='rd@%s'%extension)
    sales = Profile.objects.get(workspace=workspace, 
                                        user__username='sales@%s'%extension)
    market = Profile.objects.get(workspace=workspace, 
                                    user__username='marketing@%s'%extension)
    # main CEO tasks
    for i in ['Customer 1', 'Product A', 'Customer 2', 'Product B']:
        task = Task.objects.create(workspace=workspace, name=i,
                                   owner=ceo)
        task_nb += 1
        for (owner, name) in ( (rd, 'R&D'),
                               (market, 'Marketing'),
                               (sales, 'Sales' ) ):
            Task.objects.create(workspace=workspace, name=name,
                                owner=owner, parent=task)
            task_nb += 1
    # main managers tasks
    for i in (rd, market, sales):
        #children = i.children()
        tasks = Task.objects.filter(workspace=workspace, owner=i)
        for c in i.get_children():
            for y in range(5):
                name = "Task_%d"%n
                n += 1
                task = Task.objects.create(workspace=workspace, name=name,
                                        owner=c, parent=random.choice(tasks))
                task_nb += 1
                task_ids.append(task.id)
    # other tasks
    owners = Profile.objects.exclude(workspace=workspace,
                                     user__in=[ceo.user, rd.user,
                                               sales.user, market.user])
    if nb < task_nb:
        nb = task_nb
    while (n <= nb):
        owner = random.choice(owners)
        parent_tasks = Task.objects.filter(workspace=workspace, owner=owner.parent)
        if len(parent_tasks) > 0:
            name = "Task_%d"%n
            n += 1
            task = Task.objects.create(workspace=workspace, name=name,
                                       owner=owner,
                                       parent=random.choice(parent_tasks))
    #for n in range(nb):
        #name = "Task_%d"%n
        #if len(task_ids) > 5:
            #parent = Task.objects.get(id=random.choice(task_ids))
        #else:
            #parent=None
        #task = Task.objects.create(workspace=workspace, name=name,
                                   #owner=owner, parent=parent)
        #task_ids.append(task.id)

def clean_records(workspace):
    existing = DailyDataPerTaskPerUser.objects.filter(workspace=workspace)
    existing.delete()
    existing = DailyDataPerTask.objects.filter(workspace=workspace)
    existing.delete()
    existing = AutoRecord.objects.filter(workspace=workspace)
    existing.delete()

def generate_records(workspace, begin_date=None, end_date=None):
    tasks = Task.objects.filter(workspace=workspace)
    if tasks.count() < 1:
        return
    if end_date is None:
        end_date = datetime.datetime.today()
    if begin_date is None:
        begin_date = end_date - datetime.timedelta(10)
    nb_days = (end_date - begin_date).days
    profiles = Profile.objects.filter(workspace=workspace)
    cur = begin_date
    dailyrecord_list = []
    for profile in profiles:
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
                AutoRecord.objects.create(workspace=workspace, profile=profile,
                                      task=p, start=start, end=end)
                d = (random.uniform(7, 8) - cum)/(working_on)
                cum +=d
            cur += datetime.timedelta(1)
            ite += 1
