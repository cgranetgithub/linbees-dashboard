import datetime
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.timezone import now
from backapps.record.models import DailyRecord
from backapps.activity.models import Activity
from backapps.activity.forms import ActivityListForm
from backapps.profile.models import Profile
from frontapps.dashboard.forms import TrialForm
import libs.chart.generate_data as gen
from libs.forms import SelectForm
from libs.chart.chart import ( activities_total_time, cumulative_activity_over_time
			     , activities_over_time, users_over_time )

def check_data_existence(request):
    workspace = request.user.tenantlink.workspace
    context = {'activities_number': Activity.for_tenant(workspace
				      ).objects.filter(monitored=True).count()
	      ,'nodata': not(DailyRecord.for_tenant(workspace).objects.exists())
	      }
    some_data = context['activities_number'] != 0 and not context['nodata']
    return (context, some_data)

def has_paid(user):
    return ( user.tenantlink.workspace.paid_until + datetime.timedelta(30) ) > now().date()

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def latePayment(request):
    return render(request, 'dashboard/late_payment.html')

#@login_required
#@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
#def analysis(request):
    #return render(request, 'dashboard/analysis.html')

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
def users(request):
    (context, some_data) = check_data_existence(request)
    if some_data:
	user = request.user
	workspace = request.user.tenantlink.workspace
	pl = Profile.for_tenant(workspace).objects.all()
	choices = [ (p.user_id, p.user.email) for p in pl ]
	if request.method == 'POST':
	    form = SelectForm(request, choices=choices)
	    if form.is_valid():
		user = form.cleaned_data['ulist']
	    else:
		return redirect(reverse('dashboard:users'))
	else:
	    form = SelectForm(request, choices=choices, initial={'ulist':user.id})
	context = { 'form' : form
		  , 'form_action' : reverse('dashboard:users')}
	#activities evolution over time
	(line_data, line_options) = users_over_time(workspace, user)
	context['chart1_data'] = line_data
	context['chart1_options'] = line_options
    return render(request, 'dashboard/user.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
def activities(request):
    (context, some_data) = check_data_existence(request)
    if some_data:
	workspace = request.user.tenantlink.workspace
	plist = []
	if request.method == 'POST':
	    form = ActivityListForm(workspace, request.POST)
	    if form.is_valid():
		plist = form.cleaned_data['plist']
	else:
	    form = ActivityListForm(workspace)
	    plist = form.fields['plist'].initial
	context = { 'form' : form
		  , 'form_action' : reverse('dashboard:activities')}
	#activities time sum
	(pie_data, pie_options) = activities_total_time(workspace, plist)
	context['chart1_data'] = pie_data
	context['chart1_options'] = pie_options
	#activities evolution over time
	(line_data, line_options) = activities_over_time(workspace, plist)
	context['chart2_data'] = line_data
	context['chart2_options'] = line_options
    return render(request, 'dashboard/activity.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
def overview(request):
    (context, some_data) = check_data_existence(request)
    workspace = request.user.tenantlink.workspace
    context['workspace'] = workspace
    context['users_number'] = Profile.for_tenant(workspace).objects.filter(
							is_active=True).count()
    if some_data:
	#activities time sum
	(pie_data, pie_options) = activities_total_time(workspace)
	context['chart1_data'] = pie_data
	context['chart1_options'] = pie_options
	#activities evolution over time
	(bar_data, bar_options) = activities_over_time(workspace)
	context['chart2_data'] = bar_data
	context['chart2_options'] = bar_options
    if workspace.on_trial:
	if request.method == 'POST':
	    form = TrialForm(request.POST)
	    if form.is_valid():
		gen.clean_records(workspace)
		gen.clean_users(workspace, request.user)
		gen.generate_users(workspace  , form.cleaned_data['users'])
		gen.generate_records(workspace, form.cleaned_data['start']
					      , form.cleaned_data['end'])
		return redirect(reverse('dashboard:overview'))
	else:
	    form = TrialForm(initial={
		      'start':datetime.datetime.today()-datetime.timedelta(10)
		    , 'end':datetime.datetime.today()
		    , 'users':10})
	context['form'] = form
	context['form_action'] = reverse('dashboard:overview')
    return render(request, 'dashboard/overview.html', context)
