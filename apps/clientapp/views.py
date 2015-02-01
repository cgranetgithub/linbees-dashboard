from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as login_view
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from apps.clientapp.forms import TaskForm, ClientUserForm
from apps.profile.models import Profile
from apps.workspace.models import Workspace
from apps.record.models import AutoRecord, get_ongoing_task, new_task
from apps.task.models import Task

def client_login(request):
    return login_view(request, template_name='clientapp/login.html',
                      extra_context={'next':'/clientapp/'})

def client_register(request):
    if request.method == 'POST':
        form = ClientUserForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password2"])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(reverse('clientapp:home'))
    else:
        form = ClientUserForm()
    return render(request, 'clientapp/register.html',
                  {'form': form, 'form_action': "/clientapp/register/"})
    
@login_required(login_url=reverse_lazy('clientapp:login'))
def client_home(request):
    workspace = request.user.profile.workspace
    profile = Profile.objects.get(workspace=workspace, user=request.user)
    last_task = False
    if request.method == 'POST':
        form = TaskForm(request)
        if form.is_valid():
            if 'clock_out' in request.POST:
                task = None
            else:
                pid = form.cleaned_data['tasks']
                task = Task.objects.get(workspace=workspace, pk=pid)
            new_task(profile, task)
            return redirect(reverse('clientapp:home'))
    else:
        last_task = get_ongoing_task(profile) or False
        if last_task:
            init = {'tasks' : last_task.task.id}
        else:
            init = {'tasks' : ''}
        form = TaskForm(request, initial=init)
    records = AutoRecord.objects.filter(workspace=workspace, profile=profile
                                    ).order_by('start').reverse()[:5]
    return render(request, 'clientapp/home.html',{'form':form
                                                ,'form_action':"/clientapp/"
                                                ,'records':records
                                                ,'user':request.user
                                                ,'last_task':last_task
                                                ,'debug':settings.DEBUG})

@login_required(login_url=reverse_lazy('clientapp:login'))
def client_logout(request):
    workspace = request.user.profile.workspace
    profile = Profile.objects.get(workspace=workspace, user=request.user)
    new_task(profile, None)
    logout(request)
    return redirect(reverse('clientapp:home'))

def client_tutorial(request):
    return render(request, 'clientapp/tutorial.html')