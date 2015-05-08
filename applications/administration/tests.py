from django.contrib.auth.models import User
from workspace.models import Workspace
from profile.models import Profile, createUserProfile
from django.test.client import Client
from libs.test_util import dashboard_signup, dashboard_login, client_signup
from django_webtest import WebTest
import libs.chart.generate_data as gen

class PagesAccessTest(WebTest):
    def setUp(self):
        dashboard_signup(self.app, 'charly@lagat.com', 'secret')
    def test_pages_access(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/administration/workspace/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/administration/account/')
        self.assertEqual(response.status_code, 200)

class IsolationTest(WebTest):
    def setUp(self):
        dashboard_signup(self.app, 'user1@lagat.com', 'user1@lagat.com')
        for un in ['user2@lagat.com', 'user3@lagat.com']:
            client_signup(self.app, un, un)
        dashboard_signup(self.app, 'user1@tagal.com', 'user1@tagal.com')
        for un in ['user2@tagal.com', 'user3@tagal.com']:
            client_signup(self.app, un, un)
    def test_owner(self):
        dashboard_login(self.app, 'user1@lagat.com', 'user1@lagat.com')
        #form = self.app.get('/administration/task/new/').form
        #form['name'] = 'lagat-project'
        #form.submit()
        ws = Workspace.objects.get(name='lagat.com')
        gen.generate_records(ws)
        response = self.app.get('/user/info/')
        self.assertContains(response, '@lagat.com')
        #self.assertContains(response, 'user2@lagat.com')
        #self.assertContains(response, 'user3@lagat.com')
        #self.assertContains(response, 'lagat-project')
        self.assertNotContains(response, '@tagal.com')
        #self.assertNotContains(response, 'user2@tagal.com')
        #self.assertNotContains(response, 'user3@tagal.com')
        #self.assertNotContains(response, 'tagal-project')
        dashboard_login(self.app, 'user1@tagal.com', 'user1@tagal.com')
        #form = self.app.get('/administration/task/new/').form
        #form['name'] = 'tagal-project'
        #form.submit()
        ws = Workspace.objects.get(name='tagal.com')
        gen.generate_records(ws)
        response = self.app.get('/user/salary/')
        self.assertNotContains(response, '@lagat.com')
        #self.assertNotContains(response, 'user2@lagat.com')
        #self.assertNotContains(response, 'user3@lagat.com')
        #self.assertNotContains(response, 'lagat-project')
        self.assertContains(response, '@tagal.com')
        #self.assertContains(response, 'user2@tagal.com')
        #self.assertContains(response, 'user3@tagal.com')
        #self.assertContains(response, 'tagal-project')
        