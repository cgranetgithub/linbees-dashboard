import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.timezone import now
from backapps.record.models import ( DailyDurationPerTaskPerUser,
                                    DailyCostPerTaskPerUser )
from backapps.record.models import ( DailyDurationPerTask,
                                    DailyCostPerTask )
from backapps.task.models import Task
from backapps.profile.models import Profile
from frontapps.dashboard.forms import MultipleTaskForm
import libs.chart.generate_data as gen
#from libs.forms import SelectForm
from libs.chart.chart import (tasks_over_time, cumulative_task_over_time,
                              pie_total_time)
from libs.chart.calculus import (sum_and_sort_time, resources_involved,
                                 active_users, queryset_filter)
from frontapps.checks import has_paid, has_dashboard_access

import json

from django.http import Http404, HttpResponse

def logout_view(request):
    logout(request)
    return redirect('/')

def check_data_existence(request):
    workspace = request.user.profile.workspace
    context = {'tasks_number': Task.objects.by_workspace(workspace
                                    ).filter(monitored=True).count()
            ,'nodata':not(DailyDurationPerTaskPerUser.objects.by_workspace(workspace).exists())
            }
    some_data = context['tasks_number'] != 0 and not context['nodata']
    return (context, some_data)

#@login_required
#@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
#def analysis(request):
    #return render(request, 'dashboard/analysis.html')

@login_required
@user_passes_test(has_paid,
                  login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def overview(request):
    (context, some_data) = check_data_existence(request)
    workspace = request.user.profile.workspace
    context['workspace'] = workspace
    context['users_number'] = Profile.objects.by_workspace(workspace
                                        ).filter(user__is_active=True).count()
    if some_data:
        queryset = DailyDurationPerTaskPerUser.objects.by_workspace(workspace
                        ).filter(task__monitored=True)
        context['period'] = 90
        startd = datetime.datetime.today() - datetime.timedelta(
                                                context['period'])
        queryset = queryset_filter(queryset, startdate=startd)
        context['time_consumption'] = sum_and_sort_time(queryset, limit=3)
        context['resources_involved'] = resources_involved(queryset, limit=3)
        context['active_users'] = active_users(queryset)
        # pie chart
        (pie_data, pie_options) = pie_total_time(queryset)
        context['chart1_data'] = pie_data
        context['chart1_options'] = pie_options
    return render(request, 'dashboard/overview.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def time(request):
    (context, some_data) = check_data_existence(request)
    if some_data:
        workspace = request.user.profile.workspace
        startdate = DailyDurationPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True
                                ).order_by('date'
                                ).first().date.isoformat()
        enddate = DailyDurationPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True
                                ).order_by('date'
                                ).last().date.isoformat()
        tasks = Task.objects.by_workspace(workspace).filter(parent=None
                                            ).values_list('id', flat=True)
        context = {
                   'form_action':reverse('dashboard:time'),
                   'startdate' : startdate,
                   'enddate' : enddate,
                   'tasks' : tasks,
                   'topic' : 'time'}
    return render(request, 'dashboard/time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def get_tasks(request):
    workspace = request.user.profile.workspace
    tasks = Task.objects.by_workspace(workspace).filter(monitored=True)
    data = []
    for i in tasks:
        if i.parent is None:
            parent = '#'
        else:
            parent = i.parent.id
        data.append({'id':str(i.id),
                             'parent':str(parent),
                             'text':str(i.name)})
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def cost(request):
    (context, some_data) = check_data_existence(request)
    if some_data:
        workspace = request.user.profile.workspace
        startdate = DailyCostPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True
                                ).order_by('date'
                                ).first().date.isoformat()
        enddate = DailyCostPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True
                                ).order_by('date'
                                ).last().date.isoformat()
        tasks = Task.objects.by_workspace(workspace).filter(parent=None
                                            ).values_list('id', flat=True)
        context = {
                   'form_action':reverse('dashboard:time'),
                   'startdate' : startdate,
                   'enddate' : enddate,
                   'tasks' : tasks,
                   'topic' : 'cost'}
    return render(request, 'dashboard/cost.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def user(request):
    (context, some_data) = check_data_existence(request)
    if some_data:
        user = request.user
        workspace = request.user.profile.workspace
        pl = Profile.objects.by_workspace(workspace).all()
        choices = [ (p.user_id, p.user.email) for p in pl ]
        if request.method == 'POST':
            form = MultipleTaskForm(request, choices=choices)
            if form.is_valid():
                user = form.cleaned_data['ulist']
            else:
                return redirect(reverse('dashboard:users'))
        else:
            form = MultipleTaskForm(request, choices=choices, initial={'ulist':user.id})
        context = { 'form' : form
                , 'form_action' : reverse('dashboard:users')}
        #tasks evolution over time
        (line_data, line_options) = users_over_time(workspace, user)
        context['chart1_data'] = line_data
        context['chart1_options'] = line_options
    return render(request, 'dashboard/user.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def data_time_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = check_data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyDurationPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    queryset = queryset_filter(queryset, tasks, startdate, enddate)
    (array, line_options) = tasks_over_time(workspace, queryset, 'duration',
                                            DailyDurationPerTask)
    data['data'] = array
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def data_cumulated_time_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = check_data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyDurationPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    if tasks is not None:
        queryset = queryset.filter(task__in=tasks)
    #tasks evolution over time
    (array, line_options) = tasks_over_time(workspace, queryset, 'duration',
                                            DailyDurationPerTask)
    (line_data, line_options) = cumulative_task_over_time(array,
                                                          startdate,
                                                          enddate)
    data['data'] = line_data
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def data_cost_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = check_data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyCostPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    queryset = queryset_filter(queryset, tasks, startdate, enddate)
    (array, line_options) = tasks_over_time(workspace, queryset, 'cost',
                                            DailyCostPerTask)
    data['data'] = array
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_dashboard_access,
                  login_url=reverse_lazy('dashboard:noDashboardAccess'))
def data_cumulated_cost_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = check_data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyCostPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    if tasks is not None:
        queryset = queryset.filter(task__in=tasks)
    #tasks evolution over time
    (array, line_options) = tasks_over_time(workspace, queryset, 'cost',
                                            DailyCostPerTask)
    (line_data, line_options) = cumulative_task_over_time(array,
                                                          startdate,
                                                          enddate)
    data['data'] = line_data
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")
