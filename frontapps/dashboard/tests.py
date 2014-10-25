from django_webtest import WebTest
from django.test.client import Client
from django.core.management import call_command
from backapps.workspace.models import Workspace
from django.contrib.auth.models import User
import libs.chart.generate_data as gen

class SimpleJourneyTest(WebTest):
    def setUp(self):
        form = self.app.get('/signup/').forms[0] #form 1 is the language one
        form['username'] = 'password1@password1.com'
        form['email'] = 'password1@password1.com'
        form['password1'] = 'password1'
        form['password2'] = 'password1'
        #form['full_name'] = 'ws1'
        form.submit()
        form = self.app.get('/dashboard/task/new/').form
        form['name'] = 'p0'
        form.submit()
        form = self.app.get('/dashboard/task/new/').form
        form['name'] = 'p1'
        form.submit()
        form = self.app.get('/dashboard/task/new/').form
        form['name'] = 'p2'
        form.submit()
        ws = Workspace.objects.get(name='password1-com')
        ws.on_trial = True
        ws.save()
    def test_overview(self):
        form = self.app.get('/dashboard/login/').forms[0] #form 1 is the language one
        form['username'] = 'password1@password1.com'
        form['password'] = 'password1'
        form.submit()
        response = self.app.get('/dashboard/')
        self.assertContains(response, "password1")
        self.assertContains(response, "3 projects")
    def test_generate(self):
        form = self.app.get('/dashboard/login/').forms[0] #form 1 is the language one
        form['username'] = 'password1@password1.com'
        form['password'] = 'password1'
        form.submit()
        response = self.app.get('/dashboard/')
        self.assertContains(response, "detect")
        #generate
        call_command('populate_workspace', 'password1-com',
                     'password1@password1.com', 3, 3,
                     '2014-01-01', '2014-01-30', 'False')
        #response.form.submit() #generate
        response = self.app.get('/dashboard/')
        self.assertContains(response, "3 projects")
        #self.assertContains(response, "Task_1")
        #self.assertContains(response, "Task_2")
        response = self.app.get('/dashboard/time/')
        self.assertContains(response, "Task_0")
        self.assertContains(response, "Task_1")
        self.assertContains(response, "Task_2")
        #response = self.app.get('/dashboard/').form
        #response.submit() #generate
