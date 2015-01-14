from django import forms
from django.utils.translation import ugettext_lazy as _

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
                        label=_('Start date'),
                        widget=forms.DateInput(attrs={'class':'datepicker'}))
    end_date = forms.DateField(
                        label=_('End date'),
                        widget=forms.DateInput(attrs={'class':'datepicker'}))
