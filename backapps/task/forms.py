from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from backapps.task.models import Task
from backapps.profile.models import Profile
from mptt.forms import TreeNodeChoiceField

class TaskForm(forms.ModelForm):
    def __init__(self, ws, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        profile = user.profile
        # me and my descendant tasks
        my_descendants = profile.get_descendants(include_self=True)
        my_tasks = Task.objects.by_workspace(ws).filter(owner__in=my_descendants)
        # my manager tasks
        manager_tasks = []
        if profile.parent:
            manager_tasks = Task.objects.by_workspace(ws
                                            ).filter(owner=profile.parent)
        # exclusions (the task & its descendants)
        if self.instance is not None:
            manager_tasks = manager_tasks.exclude(id=self.instance.id)
            task_desc = self.instance.get_descendants(include_self=True)
            task_desc_ids = [ i.id for i in task_desc ]
            my_tasks = my_tasks.exclude(id__in=task_desc_ids)
        final = manager_tasks | my_tasks
        self.fields['parent'] = TreeNodeChoiceField(queryset=final,
                                                    required=False)
        self.fields['owner'] = TreeNodeChoiceField(queryset=my_descendants,
                                                    required=False)
    class Meta:
        model = Task
        fields  = ('name', 'description', 'parent', 'owner',
                   'start_date', 'end_date', 'additional_cost',
                   'cost_estimate', 'time_estimate')
        exclude = ('is_active', 'monitored', 'primary',
                   'p_group', 'p_type')
        widgets = {
            'description': forms.Textarea(attrs={'rows': '2'}),
        }

class TaskListForm(forms.Form):
    plist = forms.MultipleChoiceField(label=_('Projects')
                                    , widget=forms.CheckboxSelectMultiple)
    def __init__(self, ws, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        pl = Task.objects.by_workspace(ws).filter(monitored=True)
        self.fields['plist'].choices = ( (p.id, p.name) for p in pl )
        self.fields['plist'].initial = [ p.id for p in pl ]
