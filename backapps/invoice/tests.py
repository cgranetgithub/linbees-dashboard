from django.test import TestCase
from backapps.workspace.models import Workspace #import before tenants
from backapps.invoice.models import Invoice

class SimpleTest(TestCase):
    def setUp(self):
	self.ws = Workspace.objects.create(name='testws')
    def test_create_instance(self):
        inv = Invoice.for_tenant(self.ws).objects.create(month=1, 
							 year=2014, 
							 amount=10)
        assert inv is not None