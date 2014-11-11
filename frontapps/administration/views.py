from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from backapps.workspace.forms import WorkspaceChangeForm
#from backapps.salary.forms import FixedSalaryFormSet

@login_required
def accountAdmin(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administration:accountAdmin'))
    else:
        form = PasswordChangeForm(user)
    return render(request, 'administration/account_admin.html'
                , {'form':form, 'form_action':reverse('administration:accountAdmin')}
                )

@login_required
def workspaceAdmin(request):
    workspace = request.user.profile.workspace
    if request.method == 'POST':
        form = WorkspaceChangeForm(request.POST, instance=workspace)
        if form.is_valid():
            form.save()
            return redirect(reverse('administration:workspaceAdmin'))
    else:
        form = WorkspaceChangeForm(instance=workspace)
    return render(request, 'administration/workspace_admin.html'
                , {'form':form, 'form_action':reverse('administration:workspaceAdmin')}
                )
