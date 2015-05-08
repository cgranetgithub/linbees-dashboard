from django.test import TestCase
from workspace.models import Workspace
from payment.models import PaymentData

class SimpleTest(TestCase):
    def setUp(self):
        self.ws = Workspace.objects.create(name='testws')
    def test_create_instance(self):
        pd = PaymentData.objects.create(workspace=self.ws,
                                        key='CB num', value='2345678987654')
        assert pd is not None
