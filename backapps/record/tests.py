import datetime as dt
from decimal import Decimal
from django.utils import timezone
from django.test import TestCase
from django.test.client import Client
from django.utils.timezone import utc
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.profile.models import createUserProfile
from backapps.task.models import Task
from backapps.record.models import (AutoRecord, DailyDataPerTask,
                                    DailyDataPerTaskPerUser)

class DurationTest(TestCase):
    def test_duration(self):
        workspace = Workspace.objects.create(name='testlagatdashboard')
        auth = User.objects.create_user(username='charly@lagat.com',
                                        password='secret')
        user1 = createUserProfile(auth, workspace)
        # create 1 task & 1 record and check
        task1 = Task.objects.create(workspace=workspace, name='T1',
                                    owner=user1)
        record1 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                        profile=user1, start=timezone.now())
        record1.end = record1.start + dt.timedelta(minutes=6)
        record1.save()
        date = record1.start.date()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task1,
                                                   profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        ddtu = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                            task=task1)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        # create a sub-task with 1 record and check
        task2 = Task.objects.create(workspace=workspace, name='T2',
                                    owner=user1, parent=task1)
        record2 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                      profile=user1, start=timezone.now())
        record2.end = record2.start + dt.timedelta(minutes=12)
        record2.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task1,
                                                   profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task2,
                                                   profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.20'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('0.30'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.20'))
        # add more records to the tasks
        record3 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                            profile=user1,
                                            start=timezone.now())
        record3.end = record3.start + dt.timedelta(minutes=12)
        record3.save()
        record4 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                            profile=user1,
                                            start=timezone.now())
        record4.end = record4.start + dt.timedelta(minutes=12)
        record4.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task1,
                                                   profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.30'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task2,
                                                   profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.40'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('0.70'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.40'))
        # add new users with records
        auth = User.objects.create_user(username='john@lagat.com',
                                        password='secret')
        user2 = createUserProfile(auth, workspace)
        auth = User.objects.create_user(username='jack@lagat.com',
                                        password='secret')
        user3 = createUserProfile(auth, workspace)
        record5 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                            profile=user2, start=timezone.now())
        record5.end = record5.start + dt.timedelta(minutes=12)
        record5.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task1,
                                                   profile=user2)
        self.assertEqual(ddtu.duration, Decimal('0.20'))
        record6 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                            profile=user3, start=timezone.now())
        record6.end = record6.start + dt.timedelta(minutes=6)
        record6.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                                   date=date, task=task2,
                                                   profile=user3)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('1.00'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.50'))




    #def test_multiple_days(self):
        #record = AutoRecord.objects.create(workspace=workspace,
                                       #task=task1,
                                       #profile=user1,
                                       #start=timezone.now())
        #record.end = ( record.start
                            #+ dt.timedelta(2) )
        #record.save()
        #today = record.start.date()
        #tomorrow = today + dt.timedelta(1)
        #aftertomorrow = today + dt.timedelta(2)
        #ddtu1 = DailyDataPerTaskPerUser.objects.get(workspace=workspace, 
                                        #date=today,
                                        #task=task1,
                                        #profile=user1).duration
        #ddtu2 = DailyDataPerTaskPerUser.objects.get(workspace=workspace, 
                                        #date=tomorrow,
                                        #task=task1,
                                        #profile=user1).duration
        #self.assertEqual(ddtu2, Decimal('24'))
        #ddtu3 = DailyDataPerTaskPerUser.objects.get(workspace=workspace, 
                                        #date=aftertomorrow,
                                        #task=task1,
                                        #profile=user1).duration
        #self.assertEqual(ddtu1+ddtu2+ddtu3, Decimal('48'))

class MultipleAutoRecordADayTest(TestCase):
    def test_duration(self):
        workspace = Workspace.objects.create(name='testlagatdashboard')
        auth = User.objects.create_user(username='charly@lagat.com'
                                    , password='secret')
        user1 = createUserProfile(auth, workspace)
        task1 = Task.objects.create(workspace=workspace,
                                        name='p0', owner=user1)
        for i in range(2):
            record = AutoRecord.objects.create(workspace=workspace,
                                           task=task1, profile=user1,
                                           start=timezone.now())
            record.end = ( record.start
                                + dt.timedelta(minutes=6) )
            record.save()
        for i in range(2):
            record = AutoRecord.objects.create(workspace=workspace,
                                           task=task1, profile=user1,
                                           start=timezone.now())
            record.end = ( record.start
                                + dt.timedelta(minutes=6) )
            record.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace, 
                                        date=record.start.date()
                                        , task=task1
                                        , profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.4'))

class ApiTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatclientapp')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        ud = createUserProfile(u, workspace)
        p = Task.objects.create(workspace=workspace, name='p1', owner=ud)
        self.r = AutoRecord.objects.create(workspace=workspace, task=p,
                                           profile=ud, start=timezone.now())
    def test_get_list(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/record/')
        self.assertContains(response, "p1")
        self.assertContains(response, "meta")
        self.assertContains(response, "start")
        self.assertContains(response, "end")
    def test_get_item(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/record/%d/'%self.r.id)
        self.assertContains(response, "p1")
        self.assertContains(response, """id": %d"""%self.r.id)
        self.assertContains(response, "start")
        self.assertContains(response, "end")