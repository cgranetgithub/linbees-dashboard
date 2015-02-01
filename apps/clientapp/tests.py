from django.test import TestCase
from django_webtest import WebTest
from django.test.client import Client
from django.contrib.auth.models import User
from apps.workspace.models import Workspace, getDashboardNameFromEmail
from apps.task.models import Task
from apps.profile.models import Profile, createUserProfile
from apps.record.models import get_ongoing_task
from libs.messages import register_but_ws_does_not_exist, existing_email

class PagesAccessTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='lagat.com')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
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
        workspace = Workspace.objects.create(name='lagat.com')
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
        self.assertContains(response, "Select your current activity")
        ws = Workspace.objects.get(name='lagat.com')
        user = User.objects.get(email='charlot@lagat.com')
        assert user.is_staff is False
        assert user.is_superuser is False
        p = Profile.objects.get(user=user, workspace=ws)
        assert p.has_dashboard_access is False
        assert p.is_hr is False
        assert p.is_primary is False
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
        workspace = Workspace.objects.create(name='lagat.com')
        u = User.objects.create_user(username='charly@lagat.com'
                                    , password='secret')
        self.p = createUserProfile(u, workspace)
        self.t1 = Task.objects.create(workspace=workspace,
                                      name='task1', owner=self.p)
        self.t2 = Task.objects.create(workspace=workspace,
                                      name='task2', owner=self.p)
        c = Client()
        c.post('/i18n/setlang/', {'language':'en'})
        form = self.app.get('/clientapp/login/').forms[0]
        form['username'] = 'charly@lagat.com'
        form['password'] = 'secret'
        form.submit()
    def test_change_project(self):
        response = self.app.get('/clientapp/')
        self.assertContains(response, "task1")
        self.assertContains(response, "task2")
        self.assertNotContains(response, "task3")
        form = response.forms[0]
        form.select("tasks", self.t1.id)
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).task.name, 'task1')
        response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.select("tasks", self.t2.id)
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).task.name, 'task2')
        response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.select("tasks", self.t1.id)
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).task.name, 'task1')
    def test_set_off(self):
        response = self.app.get('/clientapp/')
        self.assertContains(response, "task1")
        self.assertContains(response, "task2")
        self.assertNotContains(response, "task3")
        form = response.forms[0]
        form.select("tasks", self.t1.id)
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).task.name, 'task1')
        
        response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.select("tasks", self.t2.id)
        form.submit()
        response = self.app.get('/clientapp/')
        form = response.forms[0]
        form.submit(name="clock_out")
        self.assertEqual(get_ongoing_task(self.p), None)
    def test_logout_close(self):
        response = self.app.get('/clientapp/')
        self.assertContains(response, "task1")
        self.assertContains(response, "task2")
        self.assertNotContains(response, "task3")
        form = response.forms[0]
        form.select("tasks", self.t1.id)
        form.submit()
        self.assertEqual(get_ongoing_task(self.p).task.name, 'task1')
        self.app.get('/clientapp/logout').follow()
        self.assertEqual(get_ongoing_task(self.p), None)
