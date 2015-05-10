from django import forms
from django.db.models.query import QuerySet
from django.utils.translation import ugettext, ugettext_lazy as _
from task.models import Task
from profile.models import Profile
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
        if self.instance is not None and self.instance.id:
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
    def clean_name(self):
        data = self.cleaned_data['name']
        # get siblings and check if name already exists
        try:
            self.instance.get_siblings().get(name=data)
        except Task.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_('A project with the same name already exists.'))
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
    def clean_parent(self):
        parent = self.cleaned_data['parent']
        print parent
        if parent:
            # verify that there is no project with same name in the parent
            try:
                parent.get_children().get(name=self.instance.name)
            except Task.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(_('A project with the same name already exists in this parent project.'))
        # Always return the cleaned data, whether you have changed it or
        # not.
        return parent
    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and (start_date > end_date):
            self.add_error('start_date', _('Start date should be lower than end date.'))
            self.add_error('end_date', _('End date should be greater than start date.'))
            
class TaskListForm(forms.Form):
    plist = forms.MultipleChoiceField(label=_('Projects')
                                    , widget=forms.CheckboxSelectMultiple)
    def __init__(self, ws, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        pl = Task.objects.filter(workspace=ws, monitored=True)
        self.fields['plist'].choices = ( (p.id, p.name) for p in pl )
        self.fields['plist'].initial = [ p.id for p in pl ]
