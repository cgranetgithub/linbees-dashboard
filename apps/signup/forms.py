from django import forms
from libs.messages import ws_already_exist
from apps.profile.models import createUserProfile
from apps.profile.forms import RegistrationForm
from apps.workspace.models import Workspace, getDashboardNameFromEmail

class SignupForm(RegistrationForm):
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        email = self.cleaned_data['email']
        ws_name = getDashboardNameFromEmail(email)
        try:
            Workspace.objects.get(name=ws_name)
        except Workspace.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(ws_already_exist%{'workspace':ws_name})
        # Always return the full collection of cleaned data.
        return cleaned_data
    def save(self):
        ws_name = getDashboardNameFromEmail(self.cleaned_data['email'])
        workspace = Workspace.objects.create(name = ws_name)
        newuser = super(SignupForm, self).save()
        profile = createUserProfile(newuser, workspace)
        profile.has_dashboard_access = True
        profile.is_hr = True
        profile.is_primary = True
        profile.save()
