import libs.chart.generate_data as gen
from django.contrib.auth.models import User
from workspace.models import Workspace
from profile.models import Profile
from django.core.management import call_command
from libs.test_util import (dashboard_signup, dashboard_login,
                            dashboard_create_task, client_signup)
from django_webtest import WebTest
import json

class SimpleJourneyTest(WebTest):
    def setUp(self):
        (response, workspace, user) = dashboard_signup(self.app,
                                                'password1@password1.com',
                                                'password1')
        dashboard_create_task(self.app, 'p0', user)
        dashboard_create_task(self.app, 'p1', user)
        dashboard_create_task(self.app, 'p2', user)
    def test_overview(self):
        dashboard_login(self.app, 'password1@password1.com', 'password1')
        response = self.app.get('/')
        self.assertContains(response, "password1")
        self.assertContains(response, "projects")
    def test_generate(self):
        dashboard_login(self.app, 'password1@password1.com', 'password1')
        response = self.app.get('/')
        self.assertContains(response, "detect")
        #generate
        call_command('populate_workspace', 'password1.com',
                     'password1@password1.com', '10', '10',
                     '2015-01-01', '2015-01-02', 'False')
        #response.form.submit() #generate
        response = self.app.get('/')
        self.assertContains(response, "projects")
        self.assertContains(response, "Task")
        #self.assertContains(response, "Task_2")
        response = self.app.get('/data/time_per_project/')
        self.assertContains(response, "Task")
        #self.assertContains(response, "Task_1")
        #self.assertContains(response, "Task_2")
        response = self.app.get('/data/cumulated_time_per_project/')
        self.assertContains(response, "Task")
        #self.assertContains(response, "Task_1")
        #self.assertContains(response, "Task_2")
        #response = self.app.get('/').form
        #response.submit() #generate

class AccessTest(WebTest):
    def setUp(self):
        # register
        dashboard_signup(self.app, 'password1@password1.com', 'password1')
        # generate data
        call_command('populate_workspace', 'password1.com',
                     'password1@password1.com', '10', '10',
                     '2015-01-01', '2015-01-02', 'False')
    def test_access(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/task/time/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/task/cost/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/task/info/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/task/new/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/user/time/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/user/info/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/user/salary/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/data/users/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/data/time_per_user/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/data/time_per_project/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/data/cost_per_project/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/data/cumulated_time_per_project/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/data/cumulated_cost_per_project/')
        self.assertEqual(response.status_code, 200)

class QueriesTest(WebTest):
    def setUp(self):
        (response, workspace, self.charly) = dashboard_signup(self.app,
                                            'charly@lagat.com', 'secret')
    def test_users(self):
        (response, workspace, john) = client_signup(self.app,
                                            'john@lagat.com', 'secret', 'john')
        john.parent = self.charly
        john.save()
        (response, workspace, jack) = client_signup(self.app,
                                            'jack@lagat.com', 'secret', 'jack')
        jack.parent = john
        jack.save()
        (response, workspace, jimy) = client_signup(self.app,
                                            'jimy@lagat.com', 'secret', 'jimy')
        jimy.parent = john
        jimy.save()
        (response, workspace, jo) = client_signup(self.app,
                                            'jo@lagat.com', 'secret', 'jo')
        jo.parent = jack
        jo.save()
        (response, workspace, jamy) = client_signup(self.app,
                                            'jamy@lagat.com', 'secret', 'jamy')
        jamy.parent = jack
        jamy.save()
        dashboard_login(self.app, 'charly@lagat.com', 'secret')
        response = self.app.get('/data/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(json.loads(response.body)), sorted([
            {u'text': u''    , u'id': str(self.charly.user.id), u'parent': u'#'},
            {u'text': u'john', u'id': str(john.user.id), u'parent': str(self.charly.user.id)},
            {u'text': u'jack', u'id': str(jack.user.id), u'parent': str(john.user.id)},
            {u'text': u'jo'  , u'id': str(jo.user.id), u'parent': str(jack.user.id)},
            {u'text': u'jamy', u'id': str(jamy.user.id), u'parent': str(jack.user.id)},
            {u'text': u'jimy', u'id': str(jimy.user.id), u'parent': str(john.user.id)}]))

    def test_tasks(self):
        (resp, task1) = dashboard_create_task(self.app, 'p1', self.charly)
        (resp, task2) = dashboard_create_task(self.app, 'p2', self.charly)
        (resp, task3) = dashboard_create_task(self.app, 'p3', self.charly, task1)
        (resp, task4) = dashboard_create_task(self.app, 'p4', self.charly, task2)
        (resp, task5) = dashboard_create_task(self.app, 'p5', self.charly, task3)
        (resp, task6) = dashboard_create_task(self.app, 'p6', self.charly, task4)
        dashboard_login(self.app, 'charly@lagat.com', 'secret')
        response = self.app.get('/data/tasks/False/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(json.loads(response.body)), sorted([
            {u'text': u'p1', u'id': str(task1.id), u'parent': [u'#'], u'state': {u'selected': u'true', u'opened': u'true'}},
            {u'text': u'p3', u'id': str(task3.id), u'parent': str(task1.id)},
            {u'text': u'p2', u'id': str(task2.id), u'parent': [u'#'], u'state': {u'selected': u'true', u'opened': u'true'}},
            {u'text': u'p4', u'id': str(task4.id), u'parent': str(task2.id)},
            {u'text': u'p5', u'id': str(task5.id), u'parent': str(task3.id)},
            {u'text': u'p6', u'id': str(task6.id), u'parent': str(task4.id)}]))

