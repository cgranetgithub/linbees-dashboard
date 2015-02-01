from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from apps.profile.models import Profile
from apps.salary.models import DailySalary
from apps.profile.forms import ProfileForm
from apps.salary.forms import SalaryFormSet
from apps.checks import has_paid, has_access, data_existence
from django.shortcuts import render
from django.core import serializers
import json
from apps.dashboard.views import STARTDATE, TODAY
from apps.dashboard.forms import DateRangeForm

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def time(request):
    (context, some_data) = data_existence(request)
    workspace = request.user.profile.workspace
    if some_data:
        user = request.user
        startdate = STARTDATE.isoformat()
        enddate = TODAY.isoformat()
        form = DateRangeForm(initial={'start_date' : startdate,
                                      'end_date'   : enddate})
        context.update({'form' : form,
                        'selection' : user.id,
                        'topic' : 'time'})
    return render(request, 'dashboard/user_time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def info(request):
    (context, some_data) = data_existence(request)
    user = request.user
    workspace = request.user.profile.workspace
    context.update({'selection' : user.id,
                    'workspace' : workspace,
                    'topic' : 'info'})
    return render(request, 'dashboard/user_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def info_edit(request, user_id):
    workspace = request.user.profile.workspace
    user = Profile.objects.get(workspace=workspace, user=user_id)
    if request.method == 'POST':
        form = ProfileForm(workspace, request.user, request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(workspace, request.user, instance=user)
    return render( request,
                   'dashboard/ajax_form.html',
                   {'form':form,
                    'form_action':reverse_lazy('user_info_edit',
                                               kwargs={'user_id': user_id})})

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def salary(request):
    (context, some_data) = data_existence(request)
    user = request.user
    workspace = request.user.profile.workspace
    context.update({'selection' : user.id,
                    'topic' : 'salary'})
    return render(request, 'dashboard/user_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def salary_edit(request, user_id):
    workspace = request.user.profile.workspace
    user = Profile.objects.get(workspace=workspace, user=user_id)
    if request.is_ajax():
        template = 'dashboard/ajax_form.html'
    else:
        template = 'dashboard/user_info.html'    
    if request.method == 'POST':
        formset = SalaryFormSet(request.POST,
                                queryset=DailySalary.objects.filter(
                                        workspace=workspace, profile=user))
        if formset.is_valid():
            fs = formset.save(commit=False)
            for i in fs:
                i.workspace = workspace
                i.profile = user
                i.save()
    else:
        formset = SalaryFormSet(queryset=DailySalary.objects.filter(
                                        workspace=workspace, profile=user))
    return render( request,
                   template,
                   {'formset':formset,
                    'is_formset':True,
                    'form_action':reverse_lazy('user_salary_edit',
                                               kwargs={'user_id': user_id})})
