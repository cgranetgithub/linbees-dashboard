from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from backapps.task.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields  = ('name', 'description')
        exclude = ('is_active', 'monitored', 'primary', 'p_group', 'p_type', 'parent')
        widgets = {
            'description': forms.Textarea(),
        }

class TaskListForm(forms.Form):
    plist = forms.MultipleChoiceField(label=_('Projects')
				    , widget=forms.CheckboxSelectMultiple)
    def __init__(self, ws, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        pl = Task.for_tenant(ws).objects.filter(monitored=True)
        self.fields['plist'].choices = ( (p.id, p.name) for p in pl )
        self.fields['plist'].initial = [ p.id for p in pl ]
