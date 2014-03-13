from django import forms
from django.utils.translation import ugettext_lazy as _

class TrialForm(forms.Form):
    start = forms.DateField(label=_('start date'))
    end   = forms.DateField(label=_('end date'))
    users = forms.DecimalField(label=_('number of users'))

class ActivityUserForm(forms.Form):
      startdate = forms.DateField(label=_('start date'))
      enddate   = forms.DateField(label=_('end date'))

      def __init__(self, request, activities, users, *args, **kwargs):
        if request.method == 'POST':
            super(ActivityUserForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(ActivityUserForm, self).__init__(*args, **kwargs)
        self.fields['activities'] = forms.MultipleChoiceField(
					  widget=forms.CheckboxSelectMultiple,
					  choices=activities, *args, **kwargs)
        self.fields['users'] = forms.MultipleChoiceField(
					  widget=forms.CheckboxSelectMultiple,
					  choices=users, *args, **kwargs)
