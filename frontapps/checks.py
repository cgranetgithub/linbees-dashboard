from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def has_paid(user):
    return True
    #return (  user.profile.workspace.paid_until
            #+ datetime.timedelta(30)               ) > now().date()

def has_dashboard_access(user):
    return user.profile.has_dashboard_access

@login_required
def latePayment(request):
    return render(request, 'dashboard/late_payment.html')

@login_required
def noDashboardAccess(request):
    return render(request, 'dashboard/no_dashboard_access.html')
