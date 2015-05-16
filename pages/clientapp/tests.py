import os

from django.test import TestCase
from django_webtest import WebTest
from django.test.client import Client
from django.contrib.auth.models import User
from workspace.models import Workspace, getDashboardNameFromEmail
from task.models import Task
from profile.models import Profile, createUserProfile
from record.models import get_ongoing_task
from libs.messages import register_but_ws_does_not_exist, existing_email
from libs.test_util import (dashboard_signup, dashboard_login,
                            dashboard_create_task, client_signup,
                            selenium_dashboard_signup,
                            selenium_client_signup, selenium_client_login,
                            selenium_dashboard_create_task)

from django.test import LiveServerTestCase
#from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        self.assertContains(response, "Select your manager")
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

class LiveTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        if "SELENIUM_USE_REMOTE" in os.environ:
            cls.selenium = webdriver.Remote(
                desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
        else:
            cls.selenium = webdriver.Firefox()
        super(LiveTest, cls).setUpClass()
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LiveTest, cls).tearDownClass()
    def wait_ajax_complete(self):
        """ Wait until ajax request is completed """
        WebDriverWait(self.selenium, 10).until(
            lambda s: s.execute_script("return jQuery.active == 0")
        )
    def setUp(self):
        (response, workspace, self.yo) = selenium_dashboard_signup(self,
                                                    'yo@test.com', 'secret')
        (response, self.task1) = selenium_dashboard_create_task(self, 'task1',
                                                                self.yo)
        (response, self.task2) = selenium_dashboard_create_task(self, 'task2',
                                                                self.yo)
        (response, workspace, self.ceo) = selenium_dashboard_signup(self,
                                                    'ceo@demo.com', 'secret')
        (response, self.task3) = selenium_dashboard_create_task(self, 'task3',
                                                                self.ceo)
        (response, self.task4) = selenium_dashboard_create_task(self, 'task4',
                                                                self.ceo)
    def test_registration(self):
        selenium_client_signup(self, 'toto@test.com', 'password')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('yo', body.text)
        self.assertNotIn('ceo', body.text)
        self.selenium.find_element_by_id('%s_anchor'%self.yo.user.id).click()
        self.selenium.find_element_by_id('validate').click()
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "clockout")))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('task1', body.text)
        self.assertIn('task2', body.text)
        self.assertNotIn('task3', body.text)
        self.assertNotIn('task4', body.text)
    def test_change_project(self):
        selenium_client_login(self, 'yo@test.com', 'secret')
        self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/'))
        self.wait_ajax_complete()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('task1', body.text)
        self.assertIn('task2', body.text)
        self.assertNotIn('task3', body.text)
        self.assertNotIn('task4', body.text)
        self.selenium.find_element_by_id('%s_anchor'%self.task1.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.yo).task.name, 'task1')
        self.selenium.find_element_by_id('%s_anchor'%self.task2.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.yo).task.name, 'task2')
        self.selenium.find_element_by_id('%s_anchor'%self.task1.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.yo).task.name, 'task1')
    def test_set_off(self):
        selenium_client_login(self, 'ceo@demo.com', 'secret')
        self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/'))
        self.wait_ajax_complete()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertNotIn('task1', body.text)
        self.assertNotIn('task2', body.text)
        self.assertIn('task3', body.text)
        self.assertIn('task4', body.text)
        self.selenium.find_element_by_id('%s_anchor'%self.task3.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.ceo).task.name, 'task3')
        self.selenium.find_element_by_id('clockout').click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.ceo), None)
    #def test_logout_close(self):
        #self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/'))
        #self.wait_ajax_complete()
        #self.selenium.find_element_by_id('%s_anchor'%self.task1.id).click()
        #self.wait_ajax_complete()
        #self.assertEqual(get_ongoing_task(self.user).task.name, 'task1')
        #self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/logout'))
        #self.assertEqual(get_ongoing_task(self.user), None)
