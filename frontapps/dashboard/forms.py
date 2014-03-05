from django import forms
from django.utils.translation import ugettext_lazy as _

class TrialForm(forms.Form):
    start = forms.DateField(label=_('start date'))
    end   = forms.DateField(label=_('end date'))
    users = forms.DecimalField(label=_('number of users'))
