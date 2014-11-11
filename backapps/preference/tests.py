from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
from backapps.preference.models import Preference
from backapps.profile.models import createUserProfile

class ApiTest(TestCase):
    def setUp(self):
        workspace = Workspace.objects.create(name='testlagatclientapp')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        self.p = createUserProfile(u, workspace)
    def test_get_list(self):
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/preference/')
        self.assertContains(response, "ClientAlwaysOnTop")
        self.assertContains(response, "meta")
    def test_get_item(self):
        pref = Preference.objects.get(profile=self.p)
        c = Client()
        c.login(username='charly@lagat.com', password='secret')
        response = c.get('/api/v1/preference/%d/'%pref.id)
        self.assertContains(response, "ClientAlwaysOnTop")
        self.assertContains(response, """id": %d"""%pref.id)