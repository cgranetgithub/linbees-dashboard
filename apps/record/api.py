from tastypie import fields
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from django.conf.urls import url
from tastypie.resources import Resource, ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from apps.profile.models import Profile
from apps.record.models import AutoRecord, new_task, get_ongoing_task
from apps.task.models import Task

class RecordResource(ModelResource):
    id = fields.IntegerField(attribute='id')
    task = fields.CharField(attribute='task')
    start = fields.CharField(attribute='start')
    end = fields.CharField(attribute='end', null=True)
    class Meta:
        resource_name = 'record'
        queryset = AutoRecord.objects.all()
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
    def get_object_list(self, request):
        profile = request.user.profile
        results = AutoRecord.objects.filter(workspace=profile.workspace,
                                            profile=profile)
        return results
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/closecurrent%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('closecurrent'), name="api_closecurrent"),
            url(r"^(?P<resource_name>%s)/getcurrent%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('getcurrent'), name="api_getcurrent"),
            url(r"^(?P<resource_name>%s)/newselection%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('newselection'), name="api_newselection"),
        ]
    def closecurrent(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        #self.is_authenticated(request)
        #self.throttle_check(request)
        if request.user and request.user.is_authenticated():
            try:
                new_task(request.user.profile, None)
                return self.create_response(request, {u'success': True})
            except:
                return self.create_response(request, 
                                            {u'reason': u'Unexpected'},
                                            HttpForbidden)
        else:
            return self.create_response(
                                    request,
                                    {u'reason': u"You are not authenticated"},
                                    HttpUnauthorized )
    def getcurrent(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        #self.is_authenticated(request)
        #self.throttle_check(request)
        if request.user and request.user.is_authenticated():
            try:
                cur = get_ongoing_task(request.user.profile)
                if cur:
                    return self.create_response(request, 
                                               {u'success': True,
                                                u'current': cur.id,
                                                u'current_task': cur.task.id})
                else:
                    return self.create_response(request,
                                               {u'success': True,
                                                u'current': None,
                                                u'current_task': None})
            except:
                return self.create_response(request, 
                                            {u'reason': u'Unexpected'},
                                            HttpForbidden)
        else:
            return self.create_response(
                                    request,
                                    {u'reason': u"You are not authenticated"},
                                    HttpUnauthorized )
    def newselection(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        #self.is_authenticated(request)
        #self.throttle_check(request)
        if request.user and request.user.is_authenticated():
            try:
                tid = request.POST.get('task_id')
                task = Task.objects.get(pk=tid)
                new_task(request.user.profile, task)
                return self.create_response(request, {u'success': True})
            except:
                return self.create_response(request, 
                                            {u'reason': u'Unexpected'},
                                            HttpForbidden)
        else:
            return self.create_response(
                                    request,
                                    {u'reason': u"You are not authenticated"},
                                    HttpUnauthorized )
