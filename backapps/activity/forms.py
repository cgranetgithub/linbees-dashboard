from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from backapps.activity.models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields  = ('name', 'description')
        exclude = ('is_active', 'monitored', 'primary', 'p_group', 'p_type', 'parent')
        widgets = {
            'description': forms.Textarea(),
        }

class ActivityListForm(forms.Form):
    plist = forms.MultipleChoiceField(label=_('Activities')
				    , widget=forms.CheckboxSelectMultiple)
    def __init__(self, ws, *args, **kwargs):
        super(ActivityListForm, self).__init__(*args, **kwargs)
        pl = Activity.for_tenant(ws).objects.filter(monitored=True)
        self.fields['plist'].choices = ( (p.id, p.name) for p in pl )
        self.fields['plist'].initial = [ p.id for p in pl ]
