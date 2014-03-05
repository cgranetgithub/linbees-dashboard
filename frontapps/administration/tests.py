from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.profile.models import Profile, createUserProfile

class PagesAccessTest(TestCase):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatdashboard')
	auth = User.objects.create_user(username='charly@lagat.com'
				     , password='secret')
	createUserProfile(auth, workspace)
    def test_pages_access(self):
	c = Client()
	c.login(username='charly@lagat.com', password='secret')
	response = c.get('/administration/activity/new/')
        self.assertEqual(response.status_code, 200)
	response = c.get('/administration/workspace/')
        self.assertEqual(response.status_code, 200)
	response = c.get('/administration/account/')
        self.assertEqual(response.status_code, 200)

class IsolationTest(TestCase):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatdashboard')
	for un in ['user1@lagat.com', 'user2@lagat.com', 'user3@lagat.com']:
	    auth = User.objects.create_user(username=un,
					    email=un,
					    password='secret')
	    createUserProfile(auth, workspace)
	workspace = Workspace.objects.create(name='testtagaldashboard')
	for un in ['user1@tagal.com', 'user2@tagal.com', 'user3@tagal.com']:
	    auth = User.objects.create_user(username=un,
					    email=un,
					    password='secret')
	    createUserProfile(auth, workspace)
    def test_owner(self):
	c = Client()
	c.login(username='user1@lagat.com', password='secret')
	response = c.get('/administration/activity/new/')
        self.assertContains(response, 'user1@lagat.com')
        self.assertContains(response, 'user2@lagat.com')
        self.assertContains(response, 'user3@lagat.com')
        self.assertNotContains(response, 'user1@tagal.com')
        self.assertNotContains(response, 'user2@tagal.com')
        self.assertNotContains(response, 'user3@tagal.com')
	c = Client()
	c.login(username='user1@tagal.com', password='secret')
	response = c.get('/administration/activity/new/')
        self.assertNotContains(response, 'user1@lagat.com')
        self.assertNotContains(response, 'user2@lagat.com')
        self.assertNotContains(response, 'user3@lagat.com')
        self.assertContains(response, 'user1@tagal.com')
        self.assertContains(response, 'user2@tagal.com')
        self.assertContains(response, 'user3@tagal.com')
        