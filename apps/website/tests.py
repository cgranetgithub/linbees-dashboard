from django.test import TestCase
from django.test.client import Client
from django_webtest import WebTest

class UrlTest(TestCase):
    def test_urls(self):
	c = Client()
	response = c.get('/')
	self.assertEqual(response.status_code, 200)
	response = c.get('/website/pricing/')
	self.assertEqual(response.status_code, 200)
	response = c.get('/website/apps/')
	self.assertEqual(response.status_code, 200)
	response = c.get('/website/about/')
	self.assertEqual(response.status_code, 200)
	response = c.get('/website/contact/')
	self.assertEqual(response.status_code, 200)
	response = c.get('/website/legal/')
	self.assertEqual(response.status_code, 200)

class ContactTest(WebTest):
    def test_working_case(self):
        form = self.app.get('/website/contact/').forms[0]
        form['email'] = 'password1@password1.com'
        form['message'] = 'this is a test'
        response = form.submit()
        assert response.status == '302 FOUND'
        assert 'contact' not in response.location
