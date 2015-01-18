from django_webtest import WebTest
from django.test.client import Client
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.profile.models import Profile, createUserProfile
import libs.chart.generate_data as gen

class PagesAccessTest(WebTest):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatdashboard')
        auth = User.objects.create_user(username='charly@lagat.com'
                                    , password='secret')
        createUserProfile(auth, workspace)
    def test_pages_access(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        #response = c.get('/administration/task/new/')
        #self.assertEqual(response.status_code, 200)
        response = c.get('/administration/workspace/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/administration/account/')
        self.assertEqual(response.status_code, 200)

class IsolationTest(WebTest):
    def setUp(self):
        form = self.app.get('/signup/').forms[0] #form 1 is the language one
        form['username'] = 'user1@lagat.com'
        form['email'] = 'user1@lagat.com'
        form['password1'] = 'user1@lagat.com'
        form['password2'] = 'user1@lagat.com'
        form.submit()
        for un in ['user2@lagat.com', 'user3@lagat.com']:
            form = self.app.get('/clientapp/register/').forms[0] #form 1 is the language one
            form['username'] = un
            form['email'] = un
            form['password1'] = un
            form['password2'] = un
            form.submit()
        form = self.app.get('/signup/').forms[0] #form 1 is the language one
        form['username'] = 'user1@tagal.com'
        form['email'] = 'user1@tagal.com'
        form['password1'] = 'user1@tagal.com'
        form['password2'] = 'user1@tagal.com'
        form.submit()
        for un in ['user2@tagal.com', 'user3@tagal.com']:
            form = self.app.get('/clientapp/register/').forms[0] #form 1 is the language one
            form['username'] = un
            form['email'] = un
            form['password1'] = un
            form['password2'] = un
            form.submit()
    def test_owner(self):
        form = self.app.get('/dashboard/login/').forms[0] #form 1 is the language one
        form['username'] = 'user1@lagat.com'
        form['password'] = 'user1@lagat.com'
        form.submit()
        #form = self.app.get('/administration/task/new/').form
        #form['name'] = 'lagat-project'
        #form.submit()
        ws = Workspace.objects.get(name='lagat-com')
        gen.generate_records(ws)
        response = self.app.get('/dashboard/data/time_per_project/None/None/')
        #self.assertContains(response, 'user1@lagat.com')
        #self.assertContains(response, 'user2@lagat.com')
        #self.assertContains(response, 'user3@lagat.com')
        self.assertContains(response, 'lagat-project')
        #self.assertNotContains(response, 'user1@tagal.com')
        #self.assertNotContains(response, 'user2@tagal.com')
        #self.assertNotContains(response, 'user3@tagal.com')
        self.assertNotContains(response, 'tagal-project')
        form = self.app.get('/dashboard/login/').forms[0] #form 1 is the language one
        form['username'] = 'user1@tagal.com'
        form['password'] = 'user1@tagal.com'
        form.submit()
        #form = self.app.get('/administration/task/new/').form
        #form['name'] = 'tagal-project'
        #form.submit()
        ws = Workspace.objects.get(name='tagal-com')
        gen.generate_records(ws)
        response = self.app.get('/dashboard/data/time_per_project/None/None/')
        #self.assertNotContains(response, 'user1@lagat.com')
        #self.assertNotContains(response, 'user2@lagat.com')
        #self.assertNotContains(response, 'user3@lagat.com')
        self.assertNotContains(response, 'lagat-project')
        #self.assertContains(response, 'user1@tagal.com')
        #self.assertContains(response, 'user2@tagal.com')
        #self.assertContains(response, 'user3@tagal.com')
        self.assertContains(response, 'tagal-project')
        