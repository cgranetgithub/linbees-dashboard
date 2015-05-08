from django.test import TestCase
from workspace.models import Workspace
from department.models import Department

class SimpleTest(TestCase):
    def setUp(self):
        self.ws = Workspace.objects.create(name='testws')
    def test_create_instance(self):
        inv = Department.objects.create(workspace=self.ws,
                                        name=u'R&D',
                                        description=u'R and D dep')
        assert inv is not None
