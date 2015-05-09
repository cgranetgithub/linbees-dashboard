import datetime as dt
from decimal import Decimal
from django.utils import timezone
from django.test import TestCase
from django_webtest import WebTest
from django.test.client import Client
from django.utils.timezone import utc
from django.contrib.auth.models import User
from workspace.models import Workspace
from profile.models import createUserProfile
from salary.models import DailySalary
from task.models import Task
from record.models import (AutoRecord, DailyDataPerTask,
                                    DailyDataPerTaskPerUser)
from libs.test_util import (dashboard_signup, dashboard_login,
                            dashboard_create_task, client_signup)

class DailyDataTest(WebTest):
    def test_time_cost(self):
        (response, workspace, user1) = dashboard_signup(self.app,
                                            'charly@lagat.com', 'secret')
        # set salary
        fs = DailySalary.objects.create(workspace=workspace,
                                        profile=user1,
                                        start_date=timezone.now().date(),
                                        end_date=timezone.now().date(),
                                        daily_wage=100)
        # create 1 task & 1 record and check
        (response, task1) = dashboard_create_task(self.app, 'T1', user1)
        record1 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                         profile=user1, start=timezone.now())
        record1.end = record1.start + dt.timedelta(minutes=6)
        record1.save()
        date = record1.start.date()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task1, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        self.assertEqual(ddtu.time_ratio, Decimal('1.00'))
        self.assertEqual(ddtu.cost, Decimal('100.00'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                            task=task1)
        self.assertEqual(ddt.duration, Decimal('0.10'))
        self.assertEqual(ddt.children_duration, Decimal('0.00'))
        self.assertEqual(ddt.cost, Decimal('100.00'))
        self.assertEqual(ddt.children_cost, Decimal('0.00'))
        # create a sub-task with 1 record and check
        (response, task2) = dashboard_create_task(self.app, 'T2', user1,
                                                  parent=task1)
        record2 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                         profile=user1, start=timezone.now())
        record2.end = record2.start + dt.timedelta(minutes=12)
        record2.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task1, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        self.assertEqual(ddtu.time_ratio, Decimal('0.33'))
        self.assertEqual(ddtu.cost, Decimal('33.33'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task2, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.20'))
        self.assertEqual(ddtu.time_ratio, Decimal('0.67'))
        self.assertEqual(ddtu.cost, Decimal('66.67'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('0.30'))
        self.assertEqual(ddt.children_duration, Decimal('0.20'))
        self.assertEqual(ddt.cost, Decimal('100.00'))
        self.assertEqual(ddt.children_cost, Decimal('66.67'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.20'))
        self.assertEqual(ddt.children_duration, Decimal('0.00'))
        self.assertEqual(ddt.cost, Decimal('66.67'))
        self.assertEqual(ddt.children_cost, Decimal('0.00'))
        # add more records to the tasks
        record3 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                        profile=user1, start=timezone.now())
        record3.end = record3.start + dt.timedelta(minutes=12)
        record3.save()
        record4 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                        profile=user1, start=timezone.now())
        record4.end = record4.start + dt.timedelta(minutes=12)
        record4.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task1, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.30'))
        self.assertEqual(ddtu.time_ratio, Decimal('0.43'))
        self.assertEqual(ddtu.cost, Decimal('42.86'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task2, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.40'))
        self.assertEqual(ddtu.time_ratio, Decimal('0.57'))
        self.assertEqual(ddtu.cost, Decimal('57.14'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('0.70'))
        self.assertEqual(ddt.children_duration, Decimal('0.40'))
        self.assertEqual(ddt.cost, Decimal('100.00'))
        self.assertEqual(ddt.children_cost, Decimal('57.14'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.40'))
        self.assertEqual(ddt.children_duration, Decimal('0.00'))
        self.assertEqual(ddt.cost, Decimal('57.14'))
        self.assertEqual(ddt.children_cost, Decimal('0.00'))
        # add new users with records
        (response, workspace, user2) = client_signup(self.app,
                                                'john@lagat.com', 'secret')
        (response, workspace, user3) = client_signup(self.app,
                                                'jack@lagat.com', 'secret')
        fs = DailySalary.objects.create(workspace=workspace,
                                        profile=user2,
                                        start_date=timezone.now().date(),
                                        end_date=timezone.now().date(),
                                        daily_wage=200)
        fs = DailySalary.objects.create(workspace=workspace,
                                        profile=user3,
                                        start_date=timezone.now().date(),
                                        end_date=timezone.now().date(),
                                        daily_wage=300)
        record5 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                            profile=user2, start=timezone.now())
        record5.end = record5.start + dt.timedelta(minutes=12)
        record5.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task1, profile=user2)
        self.assertEqual(ddtu.duration, Decimal('0.20'))
        self.assertEqual(ddtu.time_ratio, Decimal('1.00'))
        self.assertEqual(ddtu.cost, Decimal('200.00'))
        record6 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                        profile=user3, start=timezone.now())
        record6.end = record6.start + dt.timedelta(minutes=6)
        record6.save()
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task2, profile=user3)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        self.assertEqual(ddtu.time_ratio, Decimal('1.00'))
        self.assertEqual(ddtu.cost, Decimal('300.00'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('1.00'))
        self.assertEqual(ddt.children_duration, Decimal('0.50'))
        self.assertEqual(ddt.cost, Decimal('600.00'))
        self.assertEqual(ddt.children_cost, Decimal('357.14'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.50'))
        self.assertEqual(ddt.children_duration, Decimal('0.00'))
        self.assertEqual(ddt.cost, Decimal('357.14'))
        self.assertEqual(ddt.children_cost, Decimal('0.00'))
        
    def test_change_salary(self):
        (response, workspace, user1) = dashboard_signup(self.app,
                                            'charly@lagat.com', 'secret')
        # set salary
        ds1 = DailySalary.objects.create(workspace=workspace,
                                        profile=user1,
                                        start_date=timezone.now().date(),
                                        end_date=timezone.now().date(),
                                        daily_wage=100)
        # create 1 task & 1 record and check
        (response, task1) = dashboard_create_task(self.app, 'T1', user1)
        record1 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                         profile=user1, start=timezone.now())
        record1.end = record1.start + dt.timedelta(minutes=6)
        record1.save()
        date = record1.start.date()
        # create a sub-task with 1 record and check
        (response, task2) = dashboard_create_task(self.app, 'T2', user1,
                                                  parent=task1)
        record2 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                         profile=user1, start=timezone.now())
        record2.end = record2.start + dt.timedelta(minutes=12)
        record2.save()
        # add more records to the tasks
        record3 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                        profile=user1, start=timezone.now())
        record3.end = record3.start + dt.timedelta(minutes=12)
        record3.save()
        record4 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                        profile=user1, start=timezone.now())
        record4.end = record4.start + dt.timedelta(minutes=12)
        record4.save()
        # add new users with records
        (response, workspace, user2) = client_signup(self.app,
                                                'john@lagat.com', 'secret')
        (response, workspace, user3) = client_signup(self.app,
                                                'jack@lagat.com', 'secret')
        ds2 = DailySalary.objects.create(workspace=workspace,
                                        profile=user2,
                                        start_date=timezone.now().date(),
                                        end_date=timezone.now().date(),
                                        daily_wage=200)
        ds3 = DailySalary.objects.create(workspace=workspace,
                                        profile=user3,
                                        start_date=timezone.now().date(),
                                        end_date=timezone.now().date(),
                                        daily_wage=300)
        record5 = AutoRecord.objects.create(workspace=workspace, task=task1,
                                            profile=user2, start=timezone.now())
        record5.end = record5.start + dt.timedelta(minutes=12)
        record5.save()
        record6 = AutoRecord.objects.create(workspace=workspace, task=task2,
                                        profile=user3, start=timezone.now())
        record6.end = record6.start + dt.timedelta(minutes=6)
        record6.save()
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('1.00'))
        self.assertEqual(ddt.children_duration, Decimal('0.50'))
        self.assertEqual(ddt.cost, Decimal('600.00'))
        self.assertEqual(ddt.children_cost, Decimal('357.14'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.50'))
        self.assertEqual(ddt.children_duration, Decimal('0.00'))
        self.assertEqual(ddt.cost, Decimal('357.14'))
        self.assertEqual(ddt.children_cost, Decimal('0.00'))
        # change salaries
        ds1.daily_wage=80
        ds1.save()
        ds2.daily_wage=60
        ds2.save()
        ds3.daily_wage=40
        ds3.save()
        # verify
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task1, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.30'))
        self.assertEqual(ddtu.time_ratio, Decimal('0.43'))
        self.assertEqual(ddtu.cost, Decimal('34.4'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task2, profile=user1)
        self.assertEqual(ddtu.duration, Decimal('0.40'))
        self.assertEqual(ddtu.time_ratio, Decimal('0.57'))
        self.assertEqual(ddtu.cost, Decimal('45.6'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task1, profile=user2)
        self.assertEqual(ddtu.duration, Decimal('0.20'))
        self.assertEqual(ddtu.time_ratio, Decimal('1.00'))
        self.assertEqual(ddtu.cost, Decimal('60.00'))
        ddtu = DailyDataPerTaskPerUser.objects.get(workspace=workspace,
                                        date=date, task=task2, profile=user3)
        self.assertEqual(ddtu.duration, Decimal('0.10'))
        self.assertEqual(ddtu.time_ratio, Decimal('1.00'))
        self.assertEqual(ddtu.cost, Decimal('40.00'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task1)
        self.assertEqual(ddt.duration, Decimal('1.00'))
        self.assertEqual(ddt.children_duration, Decimal('0.50'))
        self.assertEqual(ddt.cost, Decimal('180.00'))
        self.assertEqual(ddt.children_cost, Decimal('85.60'))
        ddt = DailyDataPerTask.objects.get(workspace=workspace, date=date,
                                           task=task2)
        self.assertEqual(ddt.duration, Decimal('0.50'))
        self.assertEqual(ddt.children_duration, Decimal('0.00'))
        self.assertEqual(ddt.cost, Decimal('85.60'))
        self.assertEqual(ddt.children_cost, Decimal('0.00'))

    def test_move_task(self):
        pass


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