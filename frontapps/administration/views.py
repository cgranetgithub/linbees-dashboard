from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from tenancy.forms import tenant_modelform_factory, tenant_modelformset_factory
from backapps.activity.models import Activity
from backapps.activity.forms import ActivityForm
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from backapps.workspace.forms import WorkspaceChangeForm
#from backapps.salary.forms import FixedSalaryFormSet
from libs.forms import SelectForm

@login_required
def accountAdmin(request):
    user = request.user
    if request.method == 'POST':
	form = PasswordChangeForm(user, request.POST)
	if form.is_valid():
	  form.save()
	  return redirect(reverse('administration:accountAdmin'))
    else:
	form = PasswordChangeForm(user)
    return render(request, 'administration/account_admin.html'
		, {'form':form, 'form_action':reverse('administration:accountAdmin')}
		)

@login_required
def workspaceAdmin(request):
    workspace = request.user.tenantlink.workspace
    if request.method == 'POST':
	form = WorkspaceChangeForm(request.POST, instance=workspace)
	if form.is_valid():
	  form.save()
	  return redirect(reverse('administration:workspaceAdmin'))
    else:
	form = WorkspaceChangeForm(instance=workspace)
    return render(request, 'administration/workspace_admin.html'
		, {'form':form, 'form_action':reverse('administration:workspaceAdmin')}
		)

#@login_required
#def userAdmin(request):
    #workspace = request.user.tenantlink.workspace
    #fsalaryformset = tenant_modelformset_factory(workspace, FixedSalaryFormSet)
    #if request.method == 'POST':
	#userform = UserChangeForm(request.POST)
	#fs = fsalaryformset(request.POST, request.FILES)
	#if fs.is_valid():
	    #instances = fs.save(commit=False)
	    #for i in instances:
		#i.user = request.user
		#i.save()
	    #return redirect(reverse('administration:userAdmin'))
    #else:
	#userform = UserChangeForm()
	#fs = fsalaryformset()
    #return render(request, 'administration/user_admin.html'
		#, {'form':userform
		  #,'formset':fs
		  #,'labels':fsalaryformset.form.base_fields.keys()
		  #,'button_name':_("Apply")
		 #})
		 
    #workspace = request.user.workspace
    #if request.method == 'POST':
	#modelformset = CustomUserFormSet(request.POST, request.FILES)
	#if modelformset.is_valid():
	    #modelformset.save()
	    #return redirect(reverse('administration:userAdmin'))
    #else:
	#modelformset = CustomUserFormSet(queryset=CustomUser.objects.filter(workspace=workspace))    
    #return render(request, 'administration/user_admin.html'
		#, {'formset':modelformset
		  #,'labels':modelformset.form.base_fields.keys()
		  #,'button_name':_("Apply")
		 #})

@login_required
def activityAdmin(request, activity_id=None):
    workspace = request.user.tenantlink.workspace
    no_activity = (Activity.for_tenant(workspace).objects.count() == 0)
    activityTenantForm = tenant_modelform_factory(workspace, ActivityForm)
    choices = Activity.for_tenant(workspace).objects.all()
    inst = None
    if activity_id:
	inst = Activity.for_tenant(workspace).objects.get(id=activity_id)
    if request.method == 'POST':
	editform = activityTenantForm(request.POST, instance=inst)
	if editform.is_valid():
	    editform.save()
	    return redirect(reverse('administration:activityNew'))
    #GET
    else:
	editform = activityTenantForm(instance=inst)
    return render(request, 'administration/activity_admin.html',
		 {'editform':editform,
		  'choices':choices,		  
		  'no_activity':no_activity
		 })
