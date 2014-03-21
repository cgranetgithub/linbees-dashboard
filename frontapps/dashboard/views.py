import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.timezone import now
from backapps.record.models import DailyRecord
from backapps.task.models import Task
from backapps.task.forms import TaskForm
from backapps.profile.models import Profile
from frontapps.dashboard.forms import TrialForm, TaskUserForm
import libs.chart.generate_data as gen
#from libs.forms import SelectForm
from libs.chart.chart import (tasks_total_time, tasks_over_time, 
			      cumulative_task_over_time)
from tenancy.forms import tenant_modelform_factory

def check_data_existence(request):
    workspace = request.user.tenantlink.workspace
    context = {'tasks_number': Task.for_tenant(workspace
				      ).objects.filter(monitored=True).count()
	      ,'nodata':not(DailyRecord.for_tenant(workspace).objects.exists())
	      }
    some_data = context['tasks_number'] != 0 and not context['nodata']
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

#@login_required
#@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
#def users(request):
    #(context, some_data) = check_data_existence(request)
    #if some_data:
	#user = request.user
	#workspace = request.user.tenantlink.workspace
	#pl = Profile.for_tenant(workspace).objects.all()
	#choices = [ (p.user_id, p.user.email) for p in pl ]
	#if request.method == 'POST':
	    #form = SelectForm(request, choices=choices)
	    #if form.is_valid():
		#user = form.cleaned_data['ulist']
	    #else:
		#return redirect(reverse('dashboard:users'))
	#else:
	    #form = SelectForm(request, choices=choices, initial={'ulist':user.id})
	#context = { 'form' : form
		  #, 'form_action' : reverse('dashboard:users')}
	##tasks evolution over time
	#(line_data, line_options) = users_over_time(workspace, user)
	#context['chart1_data'] = line_data
	#context['chart1_options'] = line_options
    #return render(request, 'dashboard/user.html', context)

@login_required
def taskAdmin(request, task_id=None):
    workspace = request.user.tenantlink.workspace
    #no_task =    (Task.for_tenant(workspace).objects.count() == 0)
    no_task = not(Task.for_tenant(workspace).objects.exists())
    taskTenantForm = tenant_modelform_factory(workspace, TaskForm)
    choices = Task.for_tenant(workspace).objects.all()
    inst = None
    if task_id:
	inst = Task.for_tenant(workspace).objects.get(id=task_id)
    if request.method == 'POST':
	editform = taskTenantForm(request.POST, instance=inst)
	if editform.is_valid():
	    new_task = editform.save(commit=False)
	    p = Profile.for_tenant(workspace).objects.get(user=request.user)
	    new_task.owner = p
	    new_task.save()
	    return redirect(reverse('dashboard:taskNew'))
    #GET
    else:
	editform = taskTenantForm(instance=inst)
    return render(request, 'dashboard/task_admin.html',
		 {'editform':editform,
		  'choices':choices,		  
		  'no_task':no_task
		 })

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
def time(request):
    (context, some_data) = check_data_existence(request)
    if some_data:
	workspace = request.user.tenantlink.workspace
	al = Task.for_tenant(workspace).objects.filter(monitored=True)
	a_choices = ( (p.id, p.name) for p in al )
	ul = Profile.for_tenant(workspace).objects.all()
	u_choices = ( (p.user_id, p.user.email) for p in ul )
	a_select  = None
	u_select  = None
	startdate = None
	enddate   = None
	if request.method == 'POST':
	    form = TaskUserForm(request, tasks=a_choices, users=u_choices)
	    if form.is_valid():
		a_select  = form.cleaned_data['tasks']
		u_select  = form.cleaned_data['users']
		startdate = form.cleaned_data['startdate']
		enddate   = form.cleaned_data['enddate']
	else:
	    form = TaskUserForm(request, tasks=a_choices, users=u_choices)
	context = {'form' : form,
		   'form_action'   : reverse('dashboard:time')}
	#tasks time sum
	(pie_data, pie_options) = tasks_total_time(workspace, 
							a_select, u_select,
							startdate, enddate)
	context['chart1_data'] = pie_data
	context['chart1_options'] = pie_options
	#tasks evolution over time
	(line_data, line_options) = tasks_over_time(workspace, 
							 a_select, u_select,
							 startdate, enddate)
	context['chart2_data'] = line_data
	context['chart2_options'] = line_options
    return render(request, 'dashboard/time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
def overview(request):
    (context, some_data) = check_data_existence(request)
    workspace = request.user.tenantlink.workspace
    context['workspace'] = workspace
    context['users_number'] = Profile.for_tenant(workspace).objects.filter(
							is_active=True).count()
    if some_data:
	#tasks time sum
	(pie_data, pie_options) = tasks_total_time(workspace)
	context['chart1_data'] = pie_data
	context['chart1_options'] = pie_options
	#tasks evolution over time
	(bar_data, bar_options) = tasks_over_time(workspace)
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
