from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from libs.chart.calculus import queryset_filter
from profile.models import Profile
from record.models import (DailyDataPerTaskPerUser,
                                    DailyDataPerTask)
from libs.chart.chart import over_time, cumulative_over_time
#from task.models import Task
from django.db.models import Sum
from pages.checks import has_paid, has_access, data_existence
from django.http import HttpResponse
import json
from django.apps import apps

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def users(request):
    profile = request.user.profile
    ws = profile.workspace
    users = profile.get_descendants(include_self=True)
    data = []
    for i in users:
        if i.parent is None or i == profile:
            parent = '#'
        else:
            parent = i.parent.user.id
        data.append({'id':str(i.user.id),
                     'parent':str(parent),
                     'text':i.name})
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def tasks(request, single=False):
    if single is not False:
        try:
            if single.strip() in ('False', 'false'):
                single = False
            elif single.strip() in ('True', 'true'):
                single = True
            else:
                single = False
        except:
            single = False
    profile = request.user.profile
    ws = profile.workspace
    # me and my descendant tasks
    my_descendants = profile.get_descendants(include_self=True)
    my_tasks = apps.get_model('task', 'Task').objects.filter(workspace=ws, owner__in=my_descendants)
    # my ancestors and their tasks
    ancestors = profile.get_ancestors()
    ancestors_tasks = apps.get_model('task', 'Task').objects.filter(workspace=ws, owner__in=ancestors)
    #tasks = my_tasks | descendants_tasks
    #tasks = apps.get_model('task', 'Task').objects.by_workspace(workspace).filter(monitored=True)
    data = []
    selected = False
    for i in my_tasks:
        node = {'id'  : str(i.id),
                'text': i.name}
        if i.parent is None:
            node['parent'] = '#',
            if single:
                if not selected:
                    node['state'] = {'selected': 'true',
                                    'opened'  : 'true'}
                    selected = True
            else:
                node['state'] = {'selected': 'true',
                                'opened'  : 'true'}
        else:
            node['parent'] = str(i.parent.id)
            if i.parent in ancestors_tasks:
                if single:
                    if not selected:
                        node['state'] = {'selected': 'true',
                                        'opened'  : 'true'}
                        selected = True
                else:
                    node['state'] = {'selected': 'true',
                                    'opened'  : 'true'}
                root_node = {'id'  : str(i.parent.id),
                             'text': i.parent.name,
                             'parent': '#',
                             'state': {'disabled': 'true',
                                       'opened': 'true'}}
                data.append(root_node)
        data.append(node)
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
    data = {}
    if some_data and user:
        workspace = request.user.profile.workspace
        queryset = DailyDataPerTaskPerUser.objects.filter(workspace=workspace,
                                                        profile__user=user,
                                                        task__monitored=True)
        queryset = queryset_filter(queryset, None, startdate, enddate)
        (array, line_options) = over_time(workspace, queryset, 'duration',
                                                DailyDataPerTaskPerUser)
        line_options['isStacked'] = 'true'
        data['data'] = array
        data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def time_per_project(request, topic='duration'):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    data = {}
    if some_data:
        workspace = request.user.profile.workspace
        queryset = DailyDataPerTask.objects.filter(workspace=workspace,
                                                task__monitored=True)
        queryset = queryset_filter(queryset, tasks, startdate, enddate)
        (array, line_options) = over_time(workspace, queryset, topic,
                                                DailyDataPerTask)
        data['data'] = array
        data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cost_per_project(request):
    return time_per_project(request, 'cost')
    #startdate = request.GET.get('startdate')
    #enddate = request.GET.get('enddate')
    #try:
        #tasks = json.loads(request.GET.get('tasks'))
    #except:
        #tasks = None
    #(context, some_data) = data_existence(request)
    #data = {}
    #if some_data:
        #workspace = request.user.profile.workspace
        #queryset = DailyDataPerTask.objects.filter(workspace=workspace,
                                                #task__monitored=True)
        #queryset = queryset_filter(queryset, tasks, startdate, enddate)
        #(array, line_options) = over_time(workspace, queryset, 'cost',
                                                #DailyDataPerTask)
        #data['data'] = array
        #data['options'] = line_options
    #return HttpResponse(json.dumps(data), content_type="application/json")



@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cumulated_time_per_project(request, topic='duration'):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    data = {}
    if some_data:
        workspace = request.user.profile.workspace
        queryset = DailyDataPerTask.objects.filter(workspace=workspace,
                                                task__monitored=True)
        if tasks is not None:
            queryset = queryset.filter(task__in=tasks)
        #tasks evolution over time
        (array, line_options) = over_time(workspace, queryset, topic,
                                          DailyDataPerTask)
        (line_data, line_options) = cumulative_over_time(array,
                                                         startdate, enddate)
        data['data'] = line_data
        data['options'] = line_options
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cumulated_cost_per_project(request):
    return cumulated_time_per_project(request, 'cost')
    #startdate = request.GET.get('startdate')
    #enddate = request.GET.get('enddate')
    #try:
        #tasks = json.loads(request.GET.get('tasks'))
    #except:
        #tasks = None
    #(context, some_data) = data_existence(request)
    #data = {}
    #if some_data:
        #workspace = request.user.profile.workspace
        #queryset = DailyDataPerTask.objects.filter(workspace=workspace,
                                                #task__monitored=True)
        #if tasks is not None:
            #queryset = queryset.filter(task__in=tasks)
        ##tasks evolution over time
        #(array, line_options) = over_time(workspace, queryset, 'cost',
                                                #DailyDataPerTask)
        #(line_data, line_options) = cumulative_over_time(array,
                                                            #startdate,
                                                            #enddate)
        #data['data'] = line_data
        #data['options'] = line_options
    #return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def total_time_per_project(request, topic='duration'):
    try:
        tasks = json.loads(request.GET.get('tasks'))
    except:
        tasks = None
    (context, some_data) = data_existence(request)
    data = {'data':[['Task', 'total time (hours)'],]}
    if some_data and tasks:
        workspace = request.user.profile.workspace
        task_list = apps.get_model('task', 'Task').objects.filter(workspace=workspace, pk__in=tasks)
        for i in task_list:
            data_list = DailyDataPerTask.objects.filter(workspace=workspace,
                                                        task=i)
            if len(data_list) > 0:
                if topic == 'duration':
                    tmp = [ unicode(i),
                            (data_list.aggregate(Sum(topic))['%s__sum'%topic]
                                                        ).total_seconds()/3600]
                elif topic == 'cost':
                    tmp = [unicode(i),
                        int(data_list.aggregate(Sum(topic))['%s__sum'%topic])]
                data['data'].append(tmp)
        data['options'] = {'is3D':'true', 'backgroundColor':'transparent'}
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def total_cost_per_project(request):
    return total_time_per_project(request, 'cost')
