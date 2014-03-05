from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.conf import settings
#from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from frontapps.clientapp.forms import ActivityForm, ClientUserForm
from backapps.profile.models import Profile
from backapps.workspace.models import Workspace
from backapps.record.models import Record, get_ongoing_task, new_task
from backapps.activity.models import Activity

def client_login(request):
    return auth.views.login(request, template_name='clientapp/login.html'
		, extra_context={'next':'/clientapp/'})

def client_register(request):
    if request.method == 'POST':
        form = ClientUserForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            user = auth.authenticate( username=form.cleaned_data["username"]
				    , password=form.cleaned_data["password2"])
            if user is not None and user.is_active:
		auth.login(request, user)
		return redirect(reverse('clientapp:home'))
    else:
        form = ClientUserForm()
    return render(request, 'clientapp/register.html', {'form': form
                                        , 'form_action': "/clientapp/register/"})
    
@login_required(login_url=reverse_lazy('clientapp:login'))
def client_home(request):
    workspace = request.user.tenantlink.workspace
    profile = Profile.for_tenant(workspace).objects.get(user=request.user)
    last_activity = False
    if request.method == 'POST':
        form = ActivityForm(request)
        if form.is_valid():
            if 'clock_out' in request.POST:
                activity = None
            else:
                pid = form.cleaned_data['activities']
                activity = Activity.for_tenant(workspace).objects.get(pk=pid)
            new_task(profile, activity)
            return redirect(reverse('clientapp:home'))
    else:
        last_activity = get_ongoing_task(profile) or False
        if last_activity:
            init = {'activities' : last_activity.activity.id}
        else:
            init = {'activities' : ''}
        form = ActivityForm(request, initial=init)
    records = Record.for_tenant(workspace
				    ).objects.filter(user=profile
				    ).order_by('start_original').reverse()[:5]
    return render(request, 'clientapp/home.html',{'form':form
                                                 ,'form_action':"/clientapp/"
                                                 ,'records':records
                                                 ,'user':request.user
                                                 ,'last_activity':last_activity
                                                 ,'debug':settings.DEBUG})

@login_required(login_url=reverse_lazy('clientapp:login'))
def client_logout(request):
    workspace = request.user.tenantlink.workspace
    profile = Profile.for_tenant(workspace).objects.get(user=request.user)
    new_task(profile, None)
    auth.logout(request)
    return redirect(reverse('clientapp:home'))

def client_tutorial(request):
    return render(request, 'clientapp/tutorial.html')
