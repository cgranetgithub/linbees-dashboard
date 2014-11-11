import datetime
from django.test import TestCase
from django.utils.timezone import utc
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.profile.models import createUserProfile
from backapps.task.models import Task
from backapps.record.models import Record, DailyRecord

class DurationTest(TestCase):
    def setUp(self):
        self.workspace = Workspace.objects.create(name='testlagatdashboard')
        auth = User.objects.create_user(username='charly@lagat.com'
                                    , password='secret')
        self.user = createUserProfile(auth, self.workspace)
        self.task = Task.objects.create(workspace=self.workspace,
                                        name='p0', owner=self.user)
    def test_record_and_override(self):
        record = Record.objects.create(workspace=self.workspace,
                                       task=self.task,
                                       profile=self.user)
        record.end_original = ( record.start_original
                            + datetime.timedelta(minutes=6) )
        record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date(),
                                        task=self.task,
                                        profile=self.user)
        self.assertEqual(float(dr.duration), 0.1)
        record.start_override = ( record.start_original
                            - datetime.timedelta(minutes=6) )
        record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date(),
                                        task=self.task,
                                        profile=self.user)
        self.assertEqual(float(dr.duration), 0.2)
        record.end_override = ( record.start_original
                            + datetime.timedelta(minutes=12) )
        record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date(),
                                        task=self.task,
                                        profile=self.user)
        self.assertEqual(float(dr.duration), 0.3)
    def test_multiple_days(self):
        record = Record.objects.create(workspace=self.workspace,
                                       task=self.task,
                                       profile=self.user)
        record.end_original = ( record.start_original
                            + datetime.timedelta(2) )
        record.save()
        today = record.start_original.date()
        tomorrow = today + datetime.timedelta(1)
        aftertomorrow = today + datetime.timedelta(2)
        dr1 = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=today,
                                        task=self.task,
                                        profile=self.user).duration
        dr2 = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=tomorrow,
                                        task=self.task,
                                        profile=self.user).duration
        self.assertEqual(float(dr2), 24)
        dr3 = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=aftertomorrow,
                                        task=self.task,
                                        profile=self.user).duration
        self.assertEqual(float(dr1+dr2+dr3), 48)
    def test_multiple_days_with_override(self):
        record = Record.objects.create(workspace=self.workspace,
                                       task=self.task, profile=self.user)
        record.start_override = datetime.datetime(2012, 1, 1, 12, 0, tzinfo=utc)
        record.end_override = ( record.start_override
                            + datetime.timedelta(2) )
        record.save()
        today = record.start_override.date()
        tomorrow = today + datetime.timedelta(1)
        aftertomorrow = today + datetime.timedelta(2)
        dr1 = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=today
                                        , task=self.task
                                        , profile=self.user).duration
        self.assertEqual(float(dr1), 12)
        dr2 = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=tomorrow
                                        , task=self.task
                                        , profile=self.user).duration
        self.assertEqual(float(dr2), 24)
        dr3 = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=aftertomorrow
                                        , task=self.task
                                        , profile=self.user).duration
        self.assertEqual(float(dr3), 12)

class MultipleRecordADayTest(TestCase):
    def setUp(self):
        self.workspace = Workspace.objects.create(name='testlagatdashboard')
        auth = User.objects.create_user(username='charly@lagat.com'
                                    , password='secret')
        self.user = createUserProfile(auth, self.workspace)
        self.task = Task.objects.create(workspace=self.workspace,
                                        name='p0', owner=self.user)
        for i in range(2):
            record = Record.objects.create(workspace=self.workspace,
                                           task=self.task, profile=self.user)
            record.end_original = ( record.start_original
                                + datetime.timedelta(minutes=6) )
            record.save()
    def test_no_override(self):
        for i in range(2):
            record = Record.objects.create(workspace=self.workspace,
                                           task=self.task, profile=self.user)
            record.end_original = ( record.start_original
                                + datetime.timedelta(minutes=6) )
            record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date()
                                        , task=self.task
                                        , profile=self.user)
        self.assertEqual(float(dr.duration), 0.4)
    def test_start_override(self):
        for i in range(2):
            record = Record.objects.create(workspace=self.workspace,
                                           task=self.task,
                                           profile=self.user)
            record.start_override = ( record.start_original
                                - datetime.timedelta(minutes=6) )
            record.end_original = ( record.start_original
                                + datetime.timedelta(minutes=6) )
            record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date()
                                        , task=self.task
                                        , profile=self.user)
        self.assertEqual(float(dr.duration), 0.6)
    def test_end_override(self):
        for i in range(2):
            record = Record.objects.create(workspace=self.workspace,
                                           task=self.task, profile=self.user)
            record.end_original = ( record.start_original
                                + datetime.timedelta(minutes=3) )
            record.end_override = ( record.start_original
                                + datetime.timedelta(minutes=6) )
            record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date()
                                        , task=self.task
                                        , profile=self.user)
        self.assertEqual(float(dr.duration), 0.4)
    def test_both_override(self):
        for i in range(2):
            record = Record.objects.create(workspace=self.workspace,
                                           task=self.task, profile=self.user)
            record.start_override = ( record.start_original
                                - datetime.timedelta(minutes=3) )
            record.end_original = ( record.start_original
                                + datetime.timedelta(minutes=6) )
            record.end_override = ( record.start_original
                                + datetime.timedelta(minutes=3) )
            record.save()
        dr = DailyRecord.objects.by_workspace(self.workspace).get(
                                        date=record.start_original.date()
                                        , task=self.task
                                        , profile=self.user)
        self.assertEqual(float(dr.duration), 0.4)
    