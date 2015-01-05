import json
from django.contrib.auth.decorators import login_required, user_passes_test
from backapps.task.models import Task
from backapps.profile.models import Profile
from backapps.record.models import (DailyDurationPerTaskPerUser,
                                    DailyDurationPerTask,
                                    DailyCostPerTask )
from frontapps.checks import has_paid, has_access, data_existence
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from libs.chart.chart import over_time, cumulative_over_time
from libs.chart.calculus import queryset_filter

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def users(request):
    workspace = request.user.profile.workspace
    users = Profile.objects.by_workspace(workspace)
    data = []
    for i in users:
        if i.parent is None:
            parent = '#'
        else:
            parent = i.parent.user.id
        data.append({'id':str(i.user.id),
                             'parent':str(parent),
                             'text':str(i.name)})
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def tasks(request):
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
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def time_per_user(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    user = request.GET.get('user')
    (context, some_data) = data_existence(request)
    if not some_data or user is None:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyDurationPerTaskPerUser.objects.by_workspace(workspace
                        ).filter(profile__user=user, task__monitored=True)
    queryset = queryset_filter(queryset, None, startdate, enddate)
    (array, line_options) = over_time(workspace, queryset, 'duration',
                                            DailyDurationPerTaskPerUser)
    line_options['isStacked'] = 'true'
    data['data'] = array
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def time_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyDurationPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    queryset = queryset_filter(queryset, tasks, startdate, enddate)
    (array, line_options) = over_time(workspace, queryset, 'duration',
                                            DailyDurationPerTask)
    data['data'] = array
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cumulated_time_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyDurationPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    if tasks is not None:
        queryset = queryset.filter(task__in=tasks)
    #tasks evolution over time
    (array, line_options) = over_time(workspace, queryset, 'duration',
                                            DailyDurationPerTask)
    (line_data, line_options) = cumulative_over_time(array,
                                                          startdate,
                                                          enddate)
    data['data'] = line_data
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cost_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyCostPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    queryset = queryset_filter(queryset, tasks, startdate, enddate)
    (array, line_options) = over_time(workspace, queryset, 'cost',
                                            DailyCostPerTask)
    data['data'] = array
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cumulated_cost_per_project(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    if not some_data:
        raise Http404
    data = {}
    workspace = request.user.profile.workspace
    queryset = DailyCostPerTask.objects.by_workspace(workspace
                                ).filter(task__monitored=True)
    if tasks is not None:
        queryset = queryset.filter(task__in=tasks)
    #tasks evolution over time
    (array, line_options) = over_time(workspace, queryset, 'cost',
                                            DailyCostPerTask)
    (line_data, line_options) = cumulative_over_time(array,
                                                          startdate,
                                                          enddate)
    data['data'] = line_data
    data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")
