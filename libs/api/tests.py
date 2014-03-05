from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.profile.models import createUserProfile
from backapps.activity.models import Activity
from backapps.record.models import Record

class PreferenceTest(TestCase):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatclientapp')
	u = User.objects.create_user(username='charly@lagat.com'
				     , password='secret')
	createUserProfile(u, workspace)
    def test_get_list(self):
	c = Client()
	c.login(username='charly@lagat.com', password='secret')
	response = c.get('/api/v1/preference/')
        self.assertContains(response, "ClientAlwaysOnTop")
        self.assertContains(response, "meta")
    def test_get_item(self):
	c = Client()
	c.login(username='charly@lagat.com', password='secret')
	response = c.get('/api/v1/preference/1/')
        self.assertContains(response, "ClientAlwaysOnTop")
        self.assertContains(response, """id": 1""")

class ActivityTest(TestCase):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatclientapp')
	u = User.objects.create_user(username='charly@lagat.com'
				     , password='secret')
	ud = createUserProfile(u, workspace)
	Activity.for_tenant(workspace).objects.create(name='p1', owner=ud)
    def test_get_list(self):
	c = Client()
	c.login(username='charly@lagat.com', password='secret')
	response = c.get('/api/v1/activity/')
        self.assertContains(response, "p1")
        self.assertContains(response, "meta")
    def test_get_item(self):
	c = Client()
	c.login(username='charly@lagat.com', password='secret')
	response = c.get('/api/v1/activity/1/')
        self.assertContains(response, "p1")
        self.assertContains(response, """id": 1""")

class RecordTest(TestCase):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatclientapp')
	u = User.objects.create_user(username='charly@lagat.com'
				     , password='secret')
	ud = createUserProfile(u, workspace)
	p = Activity.for_tenant(workspace).objects.create(name='p1', owner=ud)
	Record.for_tenant(workspace).objects.create(activity=p, user=ud)
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
	response = c.get('/api/v1/record/1/')
        self.assertContains(response, "p1")
        self.assertContains(response, """id": 1""")
        self.assertContains(response, "start")
        self.assertContains(response, "end")
