from django import forms
from django.utils.translation import ugettext_lazy as _

class TrialForm(forms.Form):
    start = forms.DateField(label=_('start date'))
    end   = forms.DateField(label=_('end date'))
    users = forms.DecimalField(label=_('number of users'))

class TaskUserForm(forms.Form):
    startdate = forms.DateField(label=_('start date'))
    enddate   = forms.DateField(label=_('end date'))

    def __init__(self, request, tasks, users, *args, **kwargs):
        if request.method == 'POST':
            super(TaskUserForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(TaskUserForm, self).__init__(*args, **kwargs)
        #self.fields['tasks'] = forms.MultipleChoiceField(
                                        #widget=forms.CheckboxSelectMultiple,
                                        #choices=tasks, *args, **kwargs)
        #self.fields['users'] = forms.MultipleChoiceField(
                                        #widget=forms.CheckboxSelectMultiple,
                                        #choices=users, *args, **kwargs)
