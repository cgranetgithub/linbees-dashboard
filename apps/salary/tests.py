from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from apps.workspace.models import Workspace #import before tenants
from apps.profile.models import createUserProfile
from apps.salary.models import DailySalary

class SimpleTest(TestCase):
    def setUp(self):
        self.ws = Workspace.objects.create(name='testws')
        u = User.objects.create_user(username='charly@lagat.com',
                                    password='secret')
        self.p = createUserProfile(u, self.ws)
    def test_create_instance(self):
        fs = DailySalary.objects.create(workspace=self.ws,
                                        profile=self.p,
                                        start_date=datetime.today(),
                                        end_date=datetime.today(),
                                        daily_wage=100)
        assert fs is not None
