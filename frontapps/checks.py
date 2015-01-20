from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from backapps.record.models import DailyDataPerTaskPerUser
from backapps.task.models import Task

def has_paid(user):
    return True
    #return (  user.profile.workspace.paid_until
            #+ datetime.timedelta(30)               ) > now().date()

def has_access(user):
    return user.profile.has_dashboard_access

@login_required
def latePayment(request):
    return render(request, 'dashboard/late_payment.html')

@login_required
def noAccess(request):
    return render(request, 'dashboard/no_access.html')

def data_existence(request):
    workspace = request.user.profile.workspace
    context = {'tasks_number': Task.objects.by_workspace(workspace
                                    ).filter(monitored=True).count(),
               'nodata':not(DailyDataPerTaskPerUser.objects.by_workspace(
                                                        workspace).exists()),
               'workspace':workspace
            }
    some_data = context['tasks_number'] != 0 and not context['nodata']
    return (context, some_data)

