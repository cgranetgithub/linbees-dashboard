from django import forms
from django.forms import ModelForm
#from django.utils.translation import ugettext, ugettext_lazy as _
from backapps.workspace.models import Workspace

class WorkspaceChangeForm(ModelForm):
    class Meta:
        model = Workspace
        exclude = ('on_trial', )
