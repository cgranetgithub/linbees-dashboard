from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.preference.models import Preference
from backapps.profile.models import createUserProfile
from backapps.record.models import Record
from backapps.task.models import Task

class PreferenceTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatclientapp')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        self.p = createUserProfile(u, workspace)
    def test_get_list(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/preference/')
        self.assertContains(response, "ClientAlwaysOnTop")
        self.assertContains(response, "meta")
    def test_get_item(self):
        pref = Preference.objects.get(profile=self.p)
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/preference/%d/'%pref.id)
        self.assertContains(response, "ClientAlwaysOnTop")
        self.assertContains(response, """id": %d"""%pref.id)

class TaskTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatclientapp')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        ud = createUserProfile(u, workspace)
        self.t1 = Task.objects.create(workspace=workspace, name='p1', owner=ud)
    def test_get_list(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/task/')
        self.assertContains(response, "p1")
        self.assertContains(response, "meta")
    def test_get_item(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/task/%d/'%self.t1.id)
        self.assertContains(response, "p1")
        self.assertContains(response, """id": %d"""%self.t1.id)

class RecordTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatclientapp')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        ud = createUserProfile(u, workspace)
        p = Task.objects.create(workspace=workspace, name='p1', owner=ud)
        self.r = Record.objects.create(workspace=workspace, task=p, profile=ud)
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
