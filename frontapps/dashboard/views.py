import datetime, json
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.timezone import now
from backapps.record.models import (DailyDurationPerTaskPerUser,
                                    DailyDurationPerTask,
                                    DailyCostPerTask )
from backapps.task.models import Task
from backapps.profile.models import Profile
from frontapps.dashboard.forms import MultipleTaskForm
import libs.chart.generate_data as gen
#from libs.forms import SelectForm
from libs.chart.chart import pie_total_time
from libs.chart.calculus import (sum_and_sort_time, resources_involved,
                                 active_users, queryset_filter)
from frontapps.checks import has_paid, has_access, data_existence

from django.http import Http404, HttpResponse

def logout_view(request):
    logout(request)
    return redirect('/')

#@login_required
#@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
#def analysis(request):
    #return render(request, 'dashboard/analysis.html')

@login_required
@user_passes_test(has_paid,
                  login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def overview(request):
    (context, some_data) = data_existence(request)
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
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def time(request):
    (context, some_data) = data_existence(request)
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
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def cost(request):
    (context, some_data) = data_existence(request)
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

#@login_required
#@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
#@user_passes_test(has_access,
                  #login_url=reverse_lazy('dashboard:noAccess'))
#def user(request):
    #(context, some_data) = data_existence(request)
    #if some_data:
        #user = request.user
        #workspace = request.user.profile.workspace
        #pl = Profile.objects.by_workspace(workspace).all()
        #choices = [ (p.user_id, p.user.email) for p in pl ]
        ##if request.method == 'POST':
            ##form = MultipleTaskForm(request, choices=choices)
            ##if form.is_valid():
                ##user = form.cleaned_data['ulist']
            ##else:
                ##return redirect(reverse('dashboard:users'))
        ##else:
            ##form = MultipleTaskForm(request, choices=choices, initial={'ulist':user.id})
        #context = {
            ##'form' : form,
                #'form_action' : reverse('dashboard:user')}
        ##tasks evolution over time
        #(line_data, line_options) = users_over_time(workspace, user)
        #context['chart1_data'] = line_data
        #context['chart1_options'] = line_options
    #return render(request, 'dashboard/user.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def user_time(request):
    (context, some_data) = data_existence(request)
    if some_data:
        user = request.user
        workspace = request.user.profile.workspace
        #pl = Profile.objects.by_workspace(workspace).all()
        #choices = [ (p.user_id, p.user.email) for p in pl ]
        #context = {
                #'form_action' : reverse('dashboard:user_time')}
        #(line_data, line_options) = users_over_time(workspace, user)
        #context['chart1_data'] = line_data
        #context['chart1_options'] = line_options
        context['user'] = user.id
        context['topic'] = 'time'
    return render(request, 'dashboard/user_time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def user_info(request):
    context = {}
    return render(request, 'dashboard/user_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                  login_url=reverse_lazy('dashboard:noAccess'))
def user_salary(request):
    context = {}
    return render(request, 'dashboard/user_salary.html', context)

