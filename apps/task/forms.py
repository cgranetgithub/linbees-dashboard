from django import forms
from django.db.models.query import QuerySet
from django.utils.translation import ugettext, ugettext_lazy as _
from apps.task.models import Task
from apps.profile.models import Profile
from mptt.forms import TreeNodeChoiceField
try:
    from django.utils.encoding import smart_text
except ImportError: # pragma: no cover (Django 1.4 compatibility)
    from django.utils.encoding import smart_unicode as smart_text
from django.utils.html import conditional_escape, mark_safe

class ParentModelChoiceField(TreeNodeChoiceField):
    def label_from_instance(self, obj):
        """
        This is imported from GitHub for overriding, because we want to
        display 'obj.name' and not 'obj' ('obj' alone returns the full name
        with complete hierarchy)
        """
        level_indicator = self._get_level_indicator(obj)
        return mark_safe(level_indicator + ' ' + conditional_escape(
                                                    smart_text(obj.name)))

class TaskForm(forms.ModelForm):
    def __init__(self, ws, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        profile = user.profile
        # me and my descendant tasks
        my_descendants = profile.get_descendants(include_self=True)
        my_tasks = Task.objects.filter(workspace=ws, owner__in=my_descendants)
        # my manager tasks
        manager_tasks = QuerySet(Task)
        if profile.parent:
            manager_tasks = Task.objects.filter(workspace=ws, owner=profile.parent)
        # exclusions (the task & its descendants)
        if self.instance is not None:
            manager_tasks = manager_tasks.exclude(id=self.instance.id)
            task_desc = self.instance.get_descendants(include_self=True)
            task_desc_ids = [ i.id for i in task_desc ]
            my_tasks = my_tasks.exclude(id__in=task_desc_ids)
        final = manager_tasks | my_tasks
        self.fields['parent'] = ParentModelChoiceField(
                                                    label=_('Parent project'),
                                                    queryset=final,
                                                    required=False)
        self.fields['owner'] = TreeNodeChoiceField(label=_('Project owner'),
                                                   queryset=my_descendants,
                                                   required=True)
    class Meta:
        model = Task
        fields  = ('name', 'description', 'parent', 'owner',
                   'start_date', 'end_date', 'additional_cost',
                   'cost_estimate', 'time_estimate')
        exclude = ('is_active', 'monitored', 'primary',
                   'p_group', 'p_type')
        widgets = {
            'description': forms.Textarea(attrs={'rows': '1'}),
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

class TaskListForm(forms.Form):
    plist = forms.MultipleChoiceField(label=_('Projects')
                                    , widget=forms.CheckboxSelectMultiple)
    def __init__(self, ws, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        pl = Task.objects.filter(workspace=ws, monitored=True)
        self.fields['plist'].choices = ( (p.id, p.name) for p in pl )
        self.fields['plist'].initial = [ p.id for p in pl ]
