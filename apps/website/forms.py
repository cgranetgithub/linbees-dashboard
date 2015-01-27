from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext, ugettext_lazy as _

class ContactForm(forms.Form):
    email = forms.EmailField(label=_('Your email address'))
    message = forms.CharField(widget=forms.Textarea, label=_('Your message'))
    def send_email(self):
	subject = "from the contact page"
	message = self.cleaned_data['message']
	sender = self.cleaned_data['email']
	recipients = [ email for (name, email) in settings.ADMINS ]
	send_mail(subject, message, sender, recipients)
