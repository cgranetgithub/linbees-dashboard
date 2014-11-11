from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from backapps.workspace.forms import WorkspaceChangeForm
#from backapps.salary.forms import FixedSalaryFormSet

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
    workspace = request.user.profile.workspace
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
    #workspace = request.user.profile.workspace
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

