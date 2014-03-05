from django.test import TestCase
from django_webtest import WebTest
from django.test.client import Client
from django.contrib.auth.models import User
#import workspace first!
from backapps.workspace.models import Workspace, getDashboardNameFromEmail
from backapps.activity.models import Activity
from backapps.profile.models import Profile, createUserProfile
from backapps.record.models import get_ongoing_task
from libs.messages import register_but_ws_does_not_exist, existing_email

class PagesAccessTest(TestCase):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatclientapp')
	u = User.objects.create_user(username='charly@lagat.com'
				     , password='secret')
	createUserProfile(u, workspace)	
	c = Client()
	c.post('/i18n/setlang/', {'language':'en'})
    def test_pages_access_not_connected(self):
	c = Client()
	#c.post('/i18n/setlang/', {'language':'en'})
	response = c.get('/clientapp/')
        self.assertRedirects(response, '/clientapp/login/?next=/clientapp/')
	response = c.get('/clientapp/tutorial/')
        self.assertContains(response, "tutorial")
	response = c.get('/clientapp/register/')
        self.assertContains(response, "Create")
	response = c.get('/clientapp/login/')
        self.assertContains(response, "Sign in")
    def test_pages_access_connected(self):
	c = Client()
	#c.post('/i18n/setlang/', {'language':'en'})
	c.login(username='charly@lagat.com', password='secret')
	response = c.get('/clientapp/')
        self.assertNotContains(response, "Sign in")
        self.assertNotContains(response, "Create")
	response = c.get('/clientapp/tutorial/')
        self.assertContains(response, "tutorial")
	response = c.get('/clientapp/register/')
        self.assertContains(response, "Create")
	response = c.get('/clientapp/login/')
        self.assertContains(response, "Sign in")
	c.get('/clientapp/logout/')
	response = c.get('/clientapp/')
        self.assertRedirects(response, '/clientapp/login/?next=/clientapp/')

class RegisterTest(WebTest):
    def setUp(self):
	workspace = Workspace.objects.create(name='lagat-com')
	c = Client()
	c.post('/i18n/setlang/', {'language':'en'})
    def test_register(self):
        form = self.app.get('/clientapp/register/').forms[0]
        #form['first_name'] = 'ch'
        #form['last_name'] = 'gr'
        form['username'] = 'charlot@lagat.com'
        form['email']    = 'charlot@lagat.com'
        form['password1'] = 'secret'
        form['password2'] = 'secret'
        response = form.submit().follow()
        self.assertContains(response, "History")
        ws = Workspace.objects.get(name='lagat-com')
        user = User.objects.get(email='charlot@lagat.com')
        assert user.is_staff is False
        assert user.is_superuser is False
        p = Profile.for_tenant(ws).objects.get(user=user)
        assert p.is_admin_workspace is False
        assert p.is_admin_hr is False
        assert p.is_admin_primary is False
    def test_register_but_no_ws(self):
        form = self.app.get('/clientapp/register/').forms[0]
        #form['first_name'] = 'ch'
        #form['last_name'] = 'gr'
        form['username'] = 'charlot@lagat.fr'
        form['email']    = 'charlot@lagat.fr'
        form['password1'] = 'secret'
        form['password2'] = 'secret'
        response = form.submit()
        from libs.messages import register_but_ws_does_not_exist
        self.assertContains(response, register_but_ws_does_not_exist%{
		    'workspace':getDashboardNameFromEmail('charlot@lagat.fr')})
    def test_existing_email(self):
        form = self.app.get('/clientapp/register/').forms[0]
        #form['first_name'] = 'ch'
        #form['last_name'] = 'gr'
        form['username'] = 'charlot'
        form['email']    = 'charlot@lagat.com'
        form['password1'] = 'secret'
        form['password2'] = 'secret'
        response = form.submit()
        form = self.app.get('/clientapp/register/').forms[0]
        #form['first_name'] = 'ch'
        #form['last_name'] = 'gr'
        form['username'] = 'charly'
        form['email']    = 'charlot@lagat.com'
        form['password1'] = 'secret'
        form['password2'] = 'secret'
        response = form.submit()
        self.assertContains(response, existing_email)
    def test_cancel(self):
	response = self.app.get('/clientapp/register/')
	response = response.click(description="Cancel")
	self.assertRedirects(response, '/clientapp/login/?next=/clientapp/')

class ChangeProjectTest(WebTest):
    def setUp(self):
	workspace = Workspace.objects.create(name='testlagatclientapp')
	u = User.objects.create_user(username='charly@lagat.com'
				     , password='secret')
	self.p = createUserProfile(u, workspace)
	Activity.for_tenant(workspace).objects.create(name='A1', owner=self.p)
	Activity.for_tenant(workspace).objects.create(name='A2', owner=self.p)
	c = Client()
	c.post('/i18n/setlang/', {'language':'en'})
        form = self.app.get('/clientapp/login/').forms[0]
        form['username'] = 'charly@lagat.com'
        form['password'] = 'secret'
        form.submit()
    def test_change_project(self):
	response = self.app.get('/clientapp/')
        self.assertContains(response, "A1")
        self.assertContains(response, "A2")
        self.assertNotContains(response, "A3")
        form = response.forms[0]
        form.select("activities", '1')
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).activity.name, 'A1')
	response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.select("activities", '2')
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).activity.name, 'A2')
	response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.select("activities", '1')
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).activity.name, 'A1')
    def test_set_off(self):
	response = self.app.get('/clientapp/')
        self.assertContains(response, "A1")
        self.assertContains(response, "A2")
        self.assertNotContains(response, "A3")
        form = response.forms[0]
        form.select("activities", '1')
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).activity.name, 'A1')
	response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.select("activities", '2')
        form.submit()
	response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.submit(name="clock_out")
	self.assertEqual(get_ongoing_task(self.p), None)
    def test_logout_close(self):
	response = self.app.get('/clientapp/')
        self.assertContains(response, "A1")
        self.assertContains(response, "A2")
        self.assertNotContains(response, "A3")
        form = response.forms[0]
        form.select("activities", '1')
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).activity.name, 'A1')
	self.app.get('/clientapp/logout').follow()
        self.assertEqual(get_ongoing_task(self.p), None)
