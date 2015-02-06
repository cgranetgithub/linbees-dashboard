from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from libs.chart.calculus import (sum_and_sort_time, resources_involved,
                                active_users, queryset_filter)
from apps.dashboard.views import STARTDATE
from django.views.generic import View
from apps.profile.models import Profile
from django.contrib.auth import logout
from apps.record.models import DailyDataPerTaskPerUser
from django.shortcuts import render, redirect
from libs.chart.chart import pie_total_time
from apps.checks import has_paid, has_access, data_existence
from django.http import HttpResponse

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
@user_passes_test(has_paid,
                login_url=reverse_lazy('latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('noAccess'))
def overview(request):
    (context, some_data) = data_existence(request)
    workspace = request.user.profile.workspace
    context['users_number'] = Profile.objects.filter(user__is_active=True,
                                                workspace=workspace).count()
    if some_data:
        startd = STARTDATE
        queryset = DailyDataPerTaskPerUser.objects.filter(task__monitored=True,
                                                          workspace=workspace)
        queryset = queryset_filter(queryset, startdate=startd)
        context['time_consumption'] = sum_and_sort_time(queryset, limit=3)
        context['resources_involved'] = resources_involved(queryset, limit=3)
        context['active_users'] = active_users(queryset)
        # pie chart
        #(pie_data, pie_options) = pie_total_time(queryset)
        #context['chart1_data'] = pie_data
        #context['chart1_options'] = pie_options
        context['legend1'] = _('Time repartition')
        context['legend2'] = _('Cost repartition')
    return render(request, 'dashboard/overview.html', context)

class BlankView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('connected!')
