from django_webtest import WebTest
from django.test.client import Client
from django.contrib.auth.models import User
from apps.workspace.models import Workspace
from apps.profile.models import Profile
from apps.profile.models import createUserProfile
from apps.task.models import Task
from libs.test_util import (dashboard_signup, dashboard_login,
                            dashboard_create_task)
class ApiTest(WebTest):
    def setUp(self):
        (response, workspace, user) = dashboard_signup(self.app,
                                                       'charly@lagat.com',
                                                       'secret')
        (response, self.t1) = dashboard_create_task(self.app, 'p1', user)
    def test_get_list(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/task/')
        self.assertContains(response, "p1")
        self.assertContains(response, "meta")
    def test_get_item(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/task/%d/'%self.t1.id)
        self.assertContains(response, "p1")
        self.assertContains(response, """id": %d"""%self.t1.id)
