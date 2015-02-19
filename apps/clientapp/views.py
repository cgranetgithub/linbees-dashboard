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
from django.http import HttpResponse
import json

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
    return render(request, 'clientapp/home.html')

@login_required(login_url=reverse_lazy('clientapp:login'))
def client_report(request):
    workspace = request.user.profile.workspace
    profile = Profile.objects.get(workspace=workspace, user=request.user)
    records = AutoRecord.objects.filter(workspace=workspace, profile=profile
                                            ).order_by('start').reverse()[:5]
    return render(request, 'clientapp/report.html', {'records':records})


@login_required(login_url=reverse_lazy('clientapp:login'))
def client_logout(request):
    workspace = request.user.profile.workspace
    profile = Profile.objects.get(workspace=workspace, user=request.user)
    new_task(profile, None)
    logout(request)
    return redirect(reverse('clientapp:home'))

def client_tutorial(request):
    return render(request, 'clientapp/tutorial.html')

@login_required(login_url=reverse_lazy('clientapp:login'))
def tasks(request):
    profile = request.user.profile
    ws = profile.workspace
    # my tasks + manager tasks
    owners = [profile]
    ancestors = []
    if profile.parent:
        owners.append(profile.parent)
        ancestors = profile.get_ancestors().exclude(user=profile.parent.user)
    my_tasks = Task.objects.filter(workspace=ws, owner__in=owners)
    # my ancestors and their tasks (excluding my manager)
    ancestors_tasks = Task.objects.filter(workspace=ws, owner__in=ancestors)
    data = []
    root_nodes = []
    for i in my_tasks:
        node = {'id'  : str(i.id),
                'text': str(i.name)}
        if i.parent is None:
            node['parent'] = '#',
            node['state'] = {'opened'  : 'true'}
        else:
            node['parent'] = str(i.parent.id)
            if i.parent in ancestors_tasks:
                node['state'] = {'opened'  : 'true'}
                if i.parent.id not in root_nodes:
                    root_node = {'id'  : str(i.parent.id),
                                'text': str(i.parent),
                                'parent': '#',
                                'state': {'disabled': 'true',
                                        'opened': 'true'}}
                    data.append(root_node)
                    root_nodes.append(i.parent.id)
        data.append(node)
    return HttpResponse(json.dumps(data), content_type="application/json")

