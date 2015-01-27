from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.workspace.forms import WorkspaceChangeForm
from apps.checks import has_access

@login_required
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def accountAdmin(request):
    workspace = request.user.profile.workspace
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administration:accountAdmin'))
    else:
        form = PasswordChangeForm(user)
    return render(request, 'administration/account_admin.html',
                  {'form':form,
                   'workspace':workspace,
                   'form_action':reverse('administration:accountAdmin')}
                )

@login_required
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def workspaceAdmin(request):
    workspace = request.user.profile.workspace
    if request.method == 'POST':
        form = WorkspaceChangeForm(request.POST, instance=workspace)
        if form.is_valid():
            form.save()
            return redirect(reverse('administration:workspaceAdmin'))
    else:
        form = WorkspaceChangeForm(instance=workspace)
    return render(request, 'administration/workspace_admin.html',
                  {'form':form,
                   'workspace':workspace,
                   'form_action':reverse('administration:workspaceAdmin')}
                )
