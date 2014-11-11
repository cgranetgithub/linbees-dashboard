from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.profile.models import createUserProfile
from backapps.task.models import Task

class ApiTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatclientapp')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        ud = createUserProfile(u, workspace)
        self.t1 = Task.objects.create(workspace=workspace, name='p1', owner=ud)
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