from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from backapps.record.models import DailyDurationPerTaskPerUser
from backapps.profile.models import Profile
from libs.chart.chart import pie_total_time
from libs.chart.calculus import (sum_and_sort_time, resources_involved,
                                active_users, queryset_filter)
from frontapps.checks import has_paid, has_access, data_existence
from frontapps.dashboard.views import STARTDATE

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
@user_passes_test(has_paid,
                login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def overview(request):
    (context, some_data) = data_existence(request)
    workspace = request.user.profile.workspace
    context['workspace'] = workspace
    context['users_number'] = Profile.objects.by_workspace(workspace
                                        ).filter(user__is_active=True).count()
    if some_data:
        queryset = DailyDurationPerTaskPerUser.objects.by_workspace(workspace
                        ).filter(task__monitored=True)
        #context['period'] = 90
        #startd = datetime.datetime.today() - datetime.timedelta(
                                                #context['period'])
        startd = STARTDATE
        queryset = queryset_filter(queryset, startdate=startd)
        context['time_consumption'] = sum_and_sort_time(queryset, limit=3)
        context['resources_involved'] = resources_involved(queryset, limit=3)
        context['active_users'] = active_users(queryset)
        # pie chart
        (pie_data, pie_options) = pie_total_time(queryset)
        context['chart1_data'] = pie_data
        context['chart1_options'] = pie_options
    return render(request, 'dashboard/overview.html', context)