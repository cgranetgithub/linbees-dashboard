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
        self.assertContains(response, "projects")
    def test_generate(self):
        form = self.app.get('/dashboard/login/').forms[0] #form 1 is the language one
        form['username'] = 'password1@password1.com'
        form['password'] = 'password1'
        form.submit()
        response = self.app.get('/dashboard/')
        self.assertContains(response, "detect")
        #generate
        call_command('populate_workspace', 'password1-com',
                     'password1@password1.com', 10, 10,
                     '2015-01-01', '2015-01-02', 'False')
        #response.form.submit() #generate
        response = self.app.get('/dashboard/')
        self.assertContains(response, "projects")
        self.assertContains(response, "Task")
        #self.assertContains(response, "Task_2")
        response = self.app.get('/dashboard/data/time_per_project/')
        self.assertContains(response, "Task")
        #self.assertContains(response, "Task_1")
        #self.assertContains(response, "Task_2")
        response = self.app.get('/dashboard/data/cumulated_time_per_project/')
        self.assertContains(response, "Task")
        #self.assertContains(response, "Task_1")
        #self.assertContains(response, "Task_2")
        #response = self.app.get('/dashboard/').form
        #response.submit() #generate
