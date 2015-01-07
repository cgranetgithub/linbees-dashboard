import datetime, json, urlparse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from backapps.record.models import (DailyDurationPerTaskPerUser,
                                    DailyDurationPerTask,
                                    DailyCostPerTask )
from backapps.task.models import Task
from backapps.profile.models import Profile
from backapps.salary.models import DailySalary
from backapps.salary.forms import SalaryFormSet
from backapps.profile.forms import ProfileForm
from libs.chart.chart import pie_total_time
from libs.chart.calculus import (sum_and_sort_time, resources_involved,
                                active_users, queryset_filter)
from frontapps.checks import has_paid, has_access, data_existence

from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
def logout_view(request):
    logout(request)
    return redirect('/')

#@login_required
#@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
#def analysis(request):
    #return render(request, 'dashboard/analysis.html')

TODAY = datetime.date.today()
STARTDATE = TODAY - datetime.timedelta(90)

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
        tasks = Task.objects.by_workspace(workspace).filter(parent=None
                                            ).values_list('id', flat=True)
        context = { 'startdate' : startdate,
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
        tasks = Task.objects.by_workspace(workspace).filter(parent=None
                                            ).values_list('id', flat=True)
        context = { 'startdate' : startdate,
                    'enddate' : enddate,
                    'tasks' : tasks,
                    'topic' : 'cost'}
    return render(request, 'dashboard/cost.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def user_time(request):
    (context, some_data) = data_existence(request)
    if some_data:
        user = request.user
        workspace = request.user.profile.workspace
        #startdate = DailyDurationPerTaskPerUser.objects.by_workspace(workspace
                                #).filter(task__monitored=True
                                #).order_by('date'
                                #).first().date.isoformat()
        startdate = STARTDATE.isoformat()
        #enddate = DailyDurationPerTaskPerUser.objects.by_workspace(workspace
                                #).filter(task__monitored=True
                                #).order_by('date'
                                #).last().date.isoformat()
        enddate = TODAY.isoformat()
        context = { 'startdate' : startdate,
                    'enddate' : enddate,
                    'user' : user.id,
                    'topic' : 'time'}
    return render(request, 'dashboard/user_time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def user_info(request):
    user = request.user
    context = { 'user' : user.id,
                'topic' : 'info'}
    return render(request, 'dashboard/user_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def user_info_edit(request, user_id):
    workspace = request.user.profile.workspace
    user = Profile.objects.by_workspace(workspace).get(user=user_id)
    if request.method == 'POST':
        #user = Profile.objects.by_workspace(workspace
                                    #).get(user=request.POST.get('selection'))
        #qs = urlparse.parse_qs(request.POST.get('form_data'))
        #form_data = {}
        #for i,j in qs.iteritems():
            #form_data[i] = j[0]
        #form = ProfileForm(form_data, instance=user)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            #if request.is_ajax():
                #return HttpResponse('OK')
            #else:
                #return redirect(reverse_lazy('dashboard:edit_info') +
                                    #'?user=%s'%request.POST.get('selection'))
    else:
        #user = Profile.objects.by_workspace(workspace
                                            #).get(user=request.GET['selection'])
        form = ProfileForm(instance=user)
    return render( request,
                   'dashboard/user_edit.html',
                   {'form':form,
                    'form_action':reverse_lazy('dashboard:edit_info',
                                               kwargs={'user_id': user_id})})

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def user_salary(request):
    user = request.user
    context = { 'user' : user.id,
                'topic' : 'salary'}
    return render(request, 'dashboard/user_info.html', context)

def errors_to_json(errors):
    """
    Convert a Form error list to JSON::
    """
    return dict(
            (k, map(unicode, v))
            for (k,v) in errors.iteritems()
        )

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def user_salary_edit(request, user_id):
    workspace = request.user.profile.workspace
    user = Profile.objects.by_workspace(workspace).get(user=user_id)
    if request.is_ajax():
        template = 'dashboard/user_edit.html'
    else:
        template = 'dashboard/user_info.html'    
    if request.method == 'POST':
        #user = Profile.objects.by_workspace(workspace
                                    #).get(user=request.POST.get('selection'))
        #qs = urlparse.parse_qs(request.POST.get('form_data'))
        #form_data = {}
        #for i,j in qs.iteritems():
            #form_data[i] = j[0]
        formset = SalaryFormSet(request.POST,
                                queryset=DailySalary.objects.by_workspace(
                                            workspace).filter(profile=user))
        if formset.is_valid():
            fs = formset.save()
            #print fs
            #data = formset.cleaned_data
            #print data
            data = serializers.serialize('json', fs)
            print data
            if request.is_ajax():
                print "valid, ajax"
                #return HttpResponse(data)
                #from django.http import JsonResponse
                #data = {
                #'pk': self.object.pk,
                #}
                #return JsonResponse(data)
                #return redirect(reverse_lazy('dashboard:edit_salary',
                                               #kwargs={'user_id': user_id}))
            else:
                print "valid, no ajax"
                #return redirect(reverse_lazy('dashboard:user_salary'))
                                               #kwargs={'user_id': user_id}))
        #else:
            #if request.is_ajax():
                #print "invalid, ajax"
                #print formset.errors
                #ret = {'data':[]}
                #for e in formset.errors:
                    #data = errors_to_json(e)
                    #ret['data'].append(data)
                #print ret
                #return HttpResponse(json.dumps(ret))
            #else:
                #print "invalid, no ajax"
    else:
        #user = Profile.objects.by_workspace(workspace
                                            #).get(user=request.GET['selection'])
        formset = SalaryFormSet(queryset=DailySalary.objects.by_workspace(
                                            workspace).filter(profile=user))
    return render( request,
                   template,
                   {'formset':formset,
                    'is_formset':True,
                    'form_action':reverse_lazy('dashboard:edit_salary',
                                               kwargs={'user_id': user_id})})
