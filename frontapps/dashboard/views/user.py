from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from backapps.profile.models import Profile
from backapps.salary.models import DailySalary
from backapps.profile.forms import ProfileForm
from backapps.salary.forms import SalaryFormSet
from frontapps.checks import has_paid, has_access, data_existence
from django.shortcuts import render
from django.core import serializers
import json
from frontapps.dashboard.views import STARTDATE, TODAY

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def time(request):
    (context, some_data) = data_existence(request)
    if some_data:
        user = request.user
        workspace = request.user.profile.workspace
        startdate = STARTDATE.isoformat()
        enddate = TODAY.isoformat()
        context = { 'startdate' : startdate,
                    'enddate' : enddate,
                    'selection' : user.id,
                    'topic' : 'time'}
    return render(request, 'dashboard/user_time.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def info(request):
    user = request.user
    context = { 'selection' : user.id,
                'topic' : 'info'}
    return render(request, 'dashboard/user_info.html', context)

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def info_edit(request, user_id):
    workspace = request.user.profile.workspace
    user = Profile.objects.by_workspace(workspace).get(user=user_id)
    if request.method == 'POST':
        #user = Profile.objects.by_workspace(workspace
                                    #).get(user=request.POST.get('selection'))
        #qs = urlparse.parse_qs(request.POST.get('form_data'))
        #form_data = {}
        #for i,j in qs.iteritems():
            #form_data[i] = j[0]
        #form = ProfileForm(form_data, instance=user)
        form = ProfileForm(workspace, request.user, request.POST, instance=user)
        if form.is_valid():
            form.save()
            #if request.is_ajax():
                #return HttpResponse('OK')
            #else:
                #return redirect(reverse_lazy('dashboard:edit_info') +
                                    #'?user=%s'%request.POST.get('selection'))
    else:
        #user = Profile.objects.by_workspace(workspace
                                            #).get(user=request.GET['selection'])
        form = ProfileForm(workspace, request.user, instance=user)
    return render( request,
                   'dashboard/ajax_form.html',
                   {'form':form,
                    'form_action':reverse_lazy('dashboard:user_info_edit',
                                               kwargs={'user_id': user_id})})

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def salary(request):
    user = request.user
    context = { 'selection' : user.id,
                'topic' : 'salary'}
    return render(request, 'dashboard/user_info.html', context)

def errors_to_json(errors):
    """
    Convert a Form error list to JSON::
    """
    return dict(
            (k, map(unicode, v))
            for (k,v) in errors.iteritems()
        )

@login_required
@user_passes_test(has_paid, login_url=reverse_lazy('dashboard:latePayment'))
@user_passes_test(has_access,
                login_url=reverse_lazy('dashboard:noAccess'))
def salary_edit(request, user_id):
    workspace = request.user.profile.workspace
    user = Profile.objects.by_workspace(workspace).get(user=user_id)
    if request.is_ajax():
        template = 'dashboard/ajax_form.html'
    else:
        template = 'dashboard/user_info.html'    
    if request.method == 'POST':
        #user = Profile.objects.by_workspace(workspace
                                    #).get(user=request.POST.get('selection'))
        #qs = urlparse.parse_qs(request.POST.get('form_data'))
        #form_data = {}
        #for i,j in qs.iteritems():
            #form_data[i] = j[0]
        formset = SalaryFormSet(request.POST,
                                queryset=DailySalary.objects.by_workspace(
                                            workspace).filter(profile=user))
        if formset.is_valid():
            fs = formset.save()
            #print fs
            #data = formset.cleaned_data
            #print data
            data = serializers.serialize('json', fs)
            print data
            if request.is_ajax():
                print "valid, ajax"
                #return HttpResponse(data)
                #from django.http import JsonResponse
                #data = {
                #'pk': self.object.pk,
                #}
                #return JsonResponse(data)
                #return redirect(reverse_lazy('dashboard:edit_salary',
                                               #kwargs={'user_id': user_id}))
            else:
                print "valid, no ajax"
                #return redirect(reverse_lazy('dashboard:user_salary'))
                                               #kwargs={'user_id': user_id}))
        #else:
            #if request.is_ajax():
                #print "invalid, ajax"
                #print formset.errors
                #ret = {'data':[]}
                #for e in formset.errors:
                    #data = errors_to_json(e)
                    #ret['data'].append(data)
                #print ret
                #return HttpResponse(json.dumps(ret))
            #else:
                #print "invalid, no ajax"
    else:
        #user = Profile.objects.by_workspace(workspace
                                            #).get(user=request.GET['selection'])
        formset = SalaryFormSet(queryset=DailySalary.objects.by_workspace(
                                            workspace).filter(profile=user))
    return render( request,
                   template,
                   {'formset':formset,
                    'is_formset':True,
                    'form_action':reverse_lazy('dashboard:user_salary_edit',
                                               kwargs={'user_id': user_id})})
