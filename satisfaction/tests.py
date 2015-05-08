from django.test import TestCase
from workspace.models import Workspace
from satisfaction.models import Criteria, Satisfaction
from django.contrib.auth.models import User
from workspace.models import Workspace
from profile.models import createUserProfile

class SimpleTest(TestCase):
    def setUp(self):
        self.ws = Workspace.objects.create(name='testws')
        u = User.objects.create_user(username='charly@lagat.com',
                                     password='secret')
        self.p = createUserProfile(u, self.ws)
    def test_create_instance(self):
        cri = Criteria.objects.create(workspace=self.ws,
                                      name=u'salary',
                                      description=u'satisfied by salary')
        assert cri is not None
        sat = Satisfaction.objects.create(workspace=self.ws,
                                          criteria=cri,
                                          profile=self.p)
        assert sat is not None
