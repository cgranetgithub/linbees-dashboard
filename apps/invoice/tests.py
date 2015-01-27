from django.test import TestCase
from apps.workspace.models import Workspace
from apps.invoice.models import Invoice

class SimpleTest(TestCase):
    def setUp(self):
        self.ws = Workspace.objects.create(name='testws')
    def test_create_instance(self):
        inv = Invoice.objects.create(workspace=self.ws,
                                     month=1,
                                     year=2014,
                                     amount=10)
        assert inv is not None
