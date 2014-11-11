from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace #import before tenants
from backapps.profile.models import createUserProfile
from backapps.salary.models import FixedSalary

class SimpleTest(TestCase):
    def setUp(self):
        self.ws = Workspace.objects.create(name='testws')
        u = User.objects.create_user(username='charly@lagat.com',
                                    password='secret')
        self.p = createUserProfile(u, self.ws)
    def test_create_instance(self):
        fs = FixedSalary.objects.create(workspace=self.ws,
                                        profile=self.p,
                                        start_date=datetime.today(),
                                        end_date=datetime.today(),
                                        monthly_wage=100)
        assert fs is not None
