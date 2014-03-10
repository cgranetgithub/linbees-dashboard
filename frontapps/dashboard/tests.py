from django_webtest import WebTest
from django.test.client import Client
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
        form = self.app.get('/dashboard/activity/new/').form
        form['name'] = 'p0'
        form.submit()
        form = self.app.get('/dashboard/activity/new/').form
        form['name'] = 'p1'
        form.submit()
        form = self.app.get('/dashboard/activity/new/').form
        form['name'] = 'p2'
        form.submit()
    def test_overview(self):
	c = Client()
	c.post('/i18n/setlang/', {'language':'en'})
	c.login(username='password1@password1.com', password='password1')
	response = c.get('/dashboard/')
        self.assertContains(response, "3 activities")
    def test_generate(self):
	c = Client()
	c.post('/i18n/setlang/', {'language':'en'})
	c.login(username='password1@password1.com', password='password1')
	ws = Workspace.objects.get(name="password1-com")
	gen.generate_users(ws)
	gen.generate_records(ws)
	response = c.get('/dashboard/')
        self.assertContains(response, "p0")
        self.assertContains(response, "p1")
        self.assertContains(response, "p2")
	response = c.get('/dashboard/time/')
        self.assertContains(response, "p0")
        self.assertContains(response, "p1")
        self.assertContains(response, "p2")
	#response = c.get('/dashboard/users/')
        #self.assertContains(response, "password1@password1.com")
        #self.assertContains(response, "user1@password1.com")
        #self.assertContains(response, "user2@password1.com")
