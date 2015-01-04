from django.shortcuts import render, redirect
from backapps.task.forms import TaskForm
from backapps.task.models import Task
from backapps.profile.models import Profile
from django.core.urlresolvers import reverse, reverse_lazy
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from backapps.workspace.forms import WorkspaceChangeForm
from backapps.salary.models import DailySalary
from backapps.salary.forms import SalaryFormSet
from frontapps.checks import has_paid, has_dashboard_access

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
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
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
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

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def salaryAdmin(request, profile_id=None):
    workspace = request.user.profile.workspace
    choices = Profile.objects.by_workspace(workspace).all()
    if profile_id is not None:
        inst = Profile.objects.by_workspace(workspace).get(user__id=profile_id)
    else:
        inst = choices.first()
    if request.method == 'POST':
        formset = SalaryFormSet(request.POST, request.FILES,
                            queryset=DailySalary.objects.filter(profile=inst))
        if formset.is_valid():
            formset.save()
            return redirect(reverse('administration:salaryEdit',
                                    args=[profile_id]))
    else: # == 'GET'
        formset = SalaryFormSet(queryset=DailySalary.objects.filter(
                                                            profile=inst))
    return render(request,
                  'administration/salary_admin.html',
                  {'formset':formset, 'choices':choices,})

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def taskAdmin(request, task_id=None):
    workspace = request.user.profile.workspace
    #no_task =    (Task.objects.by_workspace(workspace).count() == 0)
    #no_task = not(Task.objects.by_workspace(workspace).exists())
    #taskTenantForm = tenant_modelform_factory(workspace, TaskForm)
    taskTenantForm = TaskForm
    choices = Task.objects.by_workspace(workspace).all()
    inst = None
    if task_id:
        inst = Task.objects.by_workspace(workspace).get(id=task_id)
    if request.method == 'POST':
        editform = taskTenantForm(request.POST, instance=inst)
        if editform.is_valid():
            new_task = editform.save(commit=False)
            new_task.workspace = workspace ###maybe something to improve here
            p = Profile.objects.by_workspace(workspace).get(user=request.user)
            new_task.owner = p
            new_task.save()
            return redirect(reverse('administration:taskNew'))
    #GET
    else:
        editform = taskTenantForm(instance=inst)
    return render(request, 'administration/task_admin.html',
                {'editform':editform,
                'choices':choices,                
                #'no_task':no_task
                })
