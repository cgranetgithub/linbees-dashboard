from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from backapps.task.models import Task
from backapps.task.forms import TaskForm
from frontapps.checks import has_paid, has_access, data_existence
from frontapps.dashboard.views import STARTDATE, TODAY

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def time(request):
    (context, some_data) = data_existence(request)
    if some_data:
        workspace = request.user.profile.workspace
        #startdate = DailyDurationPerTask.objects.by_workspace(workspace
                                #).filter(task__monitored=True
                                #).order_by('date'
                                #).first().date.isoformat()
        startdate = STARTDATE.isoformat()
        #enddate = DailyDurationPerTask.objects.by_workspace(workspace
                                #).filter(task__monitored=True
                                #).order_by('date'
                                #).last().date.isoformat()
        enddate = TODAY.isoformat()
        selection = Task.objects.by_workspace(workspace).filter(parent=None
                                            ).values_list('id', flat=True)
        context = { 'startdate' : startdate,
                    'enddate' : enddate,
                    'selection' : selection,
                    'topic' : 'time'}
    return render(request, 'dashboard/task_time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def cost(request):
    (context, some_data) = data_existence(request)
    if some_data:
        workspace = request.user.profile.workspace
        #startdate = DailyCostPerTask.objects.by_workspace(workspace
                                #).filter(task__monitored=True
                                #).order_by('date'
                                #).first().date.isoformat()
        startdate = STARTDATE.isoformat()
        #enddate = DailyCostPerTask.objects.by_workspace(workspace
                                #).filter(task__monitored=True
                                #).order_by('date'
                                #).last().date.isoformat()
        enddate = TODAY.isoformat()
        selection = Task.objects.by_workspace(workspace).filter(parent=None
                                            ).values_list('id', flat=True)
        context = { 'startdate' : startdate,
                    'enddate' : enddate,
                    'selection' : selection,
                    'topic' : 'cost'}
    return render(request, 'dashboard/task_cost.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def info(request):
    workspace = request.user.profile.workspace
    selection = Task.objects.by_workspace(workspace).filter(parent=None
                                        ).first().id
    context = { 'selection' : selection,
                'topic' : 'info'}
    return render(request, 'dashboard/task_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def info_edit(request, task_id):
    workspace = request.user.profile.workspace
    task = Task.objects.by_workspace(workspace).get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(workspace, request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
    else:
        form = TaskForm(workspace, request.user, instance=task)
    return render( request,
                   'dashboard/ajax_form.html',
                   {'form':form,
                    'form_action':reverse_lazy('dashboard:task_info_edit',
                                               kwargs={'task_id': task_id})})