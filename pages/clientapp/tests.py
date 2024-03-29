# -*- coding: utf-8 -*-

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
        workspace = Workspace.objects.create(name=u'lagat.com')
        u = User.objects.create_user(username=u'charly@lagat.com',
                                     password=u'secret',
                                     first_name=u"Eugène",
                                     last_name=u"Mc Donéld")
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
        form['first_name'] = 'éàéàéàé'
        form['last_name'] = 'SDFSDFSFD SDFSFDS'
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
        form['first_name'] = 'éàéàéàé'
        form['last_name'] = 'SDFSDFSFD SDFSFDS'
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
        form['first_name'] = 'éàéàéàé'
        form['last_name'] = 'SDFSDFSFD SDFSFDS'
        form['username'] = 'charlot'
        form['email']    = 'charlot@lagat.com'
        form['password1'] = 'secret'
        form['password2'] = 'secret'
        response = form.submit()
        form = self.app.get('/clientapp/register/').forms[0]
        form['first_name'] = 'éàéàéàé'
        form['last_name'] = 'SDFSDFSFD SDFSFDS'
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
    def test_case(self):
        # register manager
        form = self.app.get('/signup/').forms[0]
        form['first_name'] = 'éàéàéàé'
        form['last_name'] = 'SDFSDFSFD SDFSFDS'
        form['username'] = 'ToTo'
        form['email'] = 'toto@UPPER.com'
        form['password1'] = 'toto'
        form['password2'] = 'toto'
        response = form.submit()
        # register user
        form = self.app.get('/clientapp/register/').forms[0]
        form['first_name'] = 'éàéàéàé'
        form['last_name'] = 'SDFSDFSFD SDFSFDS'
        form['username'] = 'charlot@upper.COM'
        form['email']    = 'charlot@upper.COM'
        form['password1'] = 'secret'
        form['password2'] = 'secret'
        response = form.submit().follow()
        self.assertContains(response, "Select your manager")
        ws = Workspace.objects.get(name='upper.com')
        user = User.objects.get(email='charlot@upper.com')
        # signin
        form = self.app.get('/clientapp/login/').forms[0]
        form['username'] = 'charlOT@uPPer.cOm'
        form['password'] = 'secret'
        response = form.submit().follow()
        self.assertContains(response, "Select your current activity")

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
                                        u'yo@test.com', u'secret', u'Yé chè-WU')
        (response, self.task1) = selenium_dashboard_create_task(self, u"à la pêche",
                                                                self.yo)
        (response, self.task2) = selenium_dashboard_create_task(self, u"l'écueil",
                                                                self.yo)
        (response, workspace, self.ceo) = selenium_dashboard_signup(self,
                                                    'ceo@demo.com', 'secret')
        (response, self.task3) = selenium_dashboard_create_task(self, u'MAJUSCULE ',
                                                                self.ceo)
        (response, self.task4) = selenium_dashboard_create_task(self, u'task4',
                                                                self.ceo)
    def test_registration(self):
        selenium_client_signup(self, 'toto@test.com', 'password')
        body = self.selenium.find_element_by_tag_name('body')
        self.wait_ajax_complete()
        self.assertIn('Yo', body.text)
        self.assertNotIn('Ceo', body.text)
        self.selenium.find_element_by_id('%s_anchor'%self.yo.user.id).click()
        self.selenium.find_element_by_id('validate').click()
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "clockout")))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn(u"à la pêche", body.text)
        self.assertIn(u"l'écueil", body.text)
        self.assertNotIn(u'MAJUSCULE', body.text)
        self.assertNotIn(u'task4', body.text)
    def test_change_project(self):
        selenium_client_login(self, 'yo@test.com', 'secret')
        self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/'))
        self.wait_ajax_complete()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn(u"à la pêche", body.text)
        self.assertIn(u"l'écueil", body.text)
        self.assertNotIn(u'MAJUSCULE', body.text)
        self.assertNotIn(u'task4', body.text)
        self.selenium.find_element_by_id('%s_anchor'%self.task1.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.yo).task.name, u"à la pêche")
        self.selenium.find_element_by_id('%s_anchor'%self.task2.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.yo).task.name, u"l'écueil")
        self.selenium.find_element_by_id('%s_anchor'%self.task1.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.yo).task.name, u"à la pêche")
    def test_set_off(self):
        selenium_client_login(self, 'ceo@demo.com', 'secret')
        self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/'))
        self.wait_ajax_complete()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertNotIn(u"à la pêche", body.text)
        self.assertNotIn(u"l'écueil", body.text)
        self.assertIn(u'MAJUSCULE', body.text)
        self.assertIn(u'task4', body.text)
        self.selenium.find_element_by_id('%s_anchor'%self.task3.id).click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.ceo).task.name, u'MAJUSCULE ')
        self.selenium.find_element_by_id('clockout').click()
        self.wait_ajax_complete()
        self.assertEqual(get_ongoing_task(self.ceo), None)
    #def test_logout_close(self):
        #self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/'))
        #self.wait_ajax_complete()
        #self.selenium.find_element_by_id('%s_anchor'%self.task1.id).click()
        #self.wait_ajax_complete()
        #self.assertEqual(get_ongoing_task(self.user).task.name, "à la pêche")
        #self.selenium.get('%s%s' % (self.live_server_url, '/clientapp/logout'))
        #self.assertEqual(get_ongoing_task(self.user), None)
