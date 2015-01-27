from django.contrib.auth.models import User
from apps.workspace.models import Workspace #import before tenants
from apps.profile.models import Profile
from django.test.client import Client
from libs.test_util import dashboard_signup
from django_webtest import WebTest
from libs.messages import ws_already_exist, public_email_not_allowed
from django.test import TestCase

class UrlTest(TestCase):
    def test_urls(self):
        c = Client()
        response = c.get('/signup/')
        self.assertContains(response, "signup")

class SignupTest(WebTest):
    #note: there are 2 forms, 0 is the signup form and 1 is the language form
    def test_working_case(self):
        (response, workspace, user) = dashboard_signup(self.app,
                                                'password1@password1.com',
                                                'password1')
        assert response.status == '302 FOUND'
        assert 'signup' not in response.location
        ws = Workspace.objects.get(name='password1-com')
        user = User.objects.get(email='password1@password1.com')
        assert user.is_staff is False
        assert user.is_superuser is False
        p = Profile.objects.get(user=user)
        assert p.has_dashboard_access is True
        assert p.is_hr is True
        assert p.is_primary is True
    def test_existing_ws_name(self):
        form = self.app.get('/website/').form
        form['language'] = 'en'
        form.submit()
        (response, workspace, user) = dashboard_signup(self.app, 'toto@password1.com', 'toto')
        (response, workspace, user) = dashboard_signup(self.app, 'titi@password1.com', 'titi')
        self.assertContains(response, ws_already_exist)
    def test_public_email(self):
        form = self.app.get('/website/').form
        form['language'] = 'en'
        form.submit()
        form = self.app.get('/signup/').forms[0]
        form['username'] = 'toto'
        form['email'] = 'toto@gmail.com'
        form['password1'] = 'toto'
        form['password2'] = 'toto'
        response = form.submit()
        self.assertContains(response, 
                            public_email_not_allowed%{'domain':u'gmail.com'})
