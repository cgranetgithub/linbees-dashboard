from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from apps.dashboard.views import STARTDATE, TODAY
from apps.dashboard.forms import DateRangeForm
from apps.record.models import DailyDataPerTask
from django.shortcuts import render, redirect
from apps.task.models import Task
from django.db.models import Sum
from apps.task.forms import TaskForm
from apps.checks import has_paid, has_access, data_existence
import json

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def time(request):
    (context, some_data) = data_existence(request)
    if some_data:
        workspace = request.user.profile.workspace
        startdate = STARTDATE.isoformat()
        enddate = TODAY.isoformat()
        form = DateRangeForm(initial={'start_date' : startdate,
                                      'end_date'   : enddate})
        context.update({'form' : form,
                        'topic' : 'time',
                        'legend1': _('Time per project (in hours)'),
                        'legend2': _('Cumulated time per project (in hours)')})
    return render(request, 'dashboard/task_chart.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def cost(request):
    (context, some_data) = data_existence(request)
    if some_data:
        workspace = request.user.profile.workspace
        startdate = STARTDATE.isoformat()
        enddate = TODAY.isoformat()
        form = DateRangeForm(initial={'start_date' : startdate,
                                      'end_date'   : enddate})
        context.update({'form' : form,
                        'topic' : 'cost',
                        'legend1': _('Cost per project'),
                        'legend2': _('Cumulated cost per project')})
    return render(request, 'dashboard/task_chart.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def comparison(request):
    (context, some_data) = data_existence(request)
    context.update({'topic' : 'control'})
    return render(request, 'dashboard/task_comparison.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def info(request):
    (context, some_data) = data_existence(request)
    context.update({'topic' : 'info'})
    return render(request, 'dashboard/task_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def info_edit(request, task_id):
    workspace = request.user.profile.workspace
    task = Task.objects.get(id=task_id, workspace=workspace)
    if request.method == 'POST':
        form = TaskForm(workspace, request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
    else:
        form = TaskForm(workspace, request.user, instance=task)
    context = {'form':form,
               'form_action':reverse_lazy('task_info_edit',
                                               kwargs={'task_id': task_id})}
    return render( request, 'dashboard/ajax_form.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def new(request):
    (context, some_data) = data_existence(request)
    workspace = request.user.profile.workspace
    if request.method == 'POST':
        form = TaskForm(workspace, request.user, request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.workspace = workspace
            new_task.save()
            return redirect(reverse_lazy('task_new'))
    else:
        form = TaskForm(workspace, request.user)
    context.update({'form':form,
                    'form_action':reverse_lazy('task_new')})
    return render(request, 'dashboard/task_new.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('noAccess'))
def comparison_table(request):
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    data = []
    if some_data and tasks:
        workspace = request.user.profile.workspace
        task_list = Task.objects.filter(workspace=workspace, pk__in=tasks)
        for i in task_list:
            if not (i.cost_estimate or i.additional_cost):
                cost = ''
            else:
                cost = (i.cost_estimate or 0) + (i.additional_cost or 0)
            if i.start_date:
                start = i.start_date.isoformat()
            else:
                start = None
            if i.end_date:
                end = i.end_date.isoformat()
            else:
                end = None
            tmp = { 'name':unicode(i),
                    'start':start, 'end':end,
                    'time':i.time_estimate or '', 'cost':cost,
                    'actual_start':'', 'actual_end':'',
                    'actual_time':'', 'actual_cost':'' }
            data_list = DailyDataPerTask.objects.filter(workspace=workspace,
                                                    task=i).order_by('date')
            if len(data_list) > 0:
                tmp['actual_start'] = data_list.first().date.isoformat()
                tmp['actual_end'] = data_list.last().date.isoformat()
                tmp['actual_time'] = float(data_list.aggregate(Sum('duration')
                                                            )['duration__sum']) or ''
                tmp['actual_cost'] = float(data_list.aggregate(Sum('cost')
                                                                )['cost__sum']) or ''
            data.append(tmp)
    context['data'] = data
    return render(request, 'dashboard/task_comparison_table.html', context)
