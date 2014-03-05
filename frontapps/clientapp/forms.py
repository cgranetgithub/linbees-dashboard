from django import forms
from libs.messages import register_but_ws_does_not_exist
#from django.utils.translation import ugettext, ugettext_lazy as _
from backapps.activity.models import Activity
from backapps.profile.models import createUserProfile
from backapps.profile.forms import RegistrationForm
from backapps.workspace.models import Workspace, getDashboardNameFromEmail

class ActivityForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        if request.method == 'POST':
            super(ActivityForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(ActivityForm, self).__init__(*args, **kwargs)
        workspace = request.user.tenantlink.workspace
        self.fields['activities'] = forms.ChoiceField(
                    widget=forms.RadioSelect(attrs={
					  'onchange': 'this.form.submit()'})
                  , choices = [ (p.id, p.name) for p in Activity.for_tenant(
						    workspace).objects.all()]
		  , label = ' ')

class ClientUserForm(RegistrationForm):
    def clean(self):
	cleaned_data = super(ClientUserForm, self).clean()
	email = self.cleaned_data['email']
	ws_name = getDashboardNameFromEmail(email)
        try:
            Workspace.objects.get(name=ws_name)
        except Workspace.DoesNotExist:
            raise forms.ValidationError(
		      register_but_ws_does_not_exist%{'workspace':ws_name})
	# Always return the full collection of cleaned data.
	return cleaned_data
    def save(self):
	ws_name = getDashboardNameFromEmail(self.cleaned_data['email'])
        workspace = Workspace.objects.get(name=ws_name)
	newuser = super(ClientUserForm, self).save()
	createUserProfile(newuser, workspace)
