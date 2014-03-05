from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from backapps.record.models import Record, new_task
from backapps.activity.models import Activity
from backapps.profile.models import Profile
from backapps.preference.models import Preference

class PreferenceResource(Resource):
    id = fields.IntegerField(attribute='id')
    key = fields.CharField(attribute='key')
    value = fields.CharField(attribute='value')
    class Meta:
        resource_name = 'preference'
        object_class = Preference
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs
    def get_object_list(self, request):
        tenant = request.user.tenantlink.workspace
	user = Profile.for_tenant(tenant).objects.get(user=request.user)
        results = Preference.for_tenant(tenant).objects.filter(user=user)
        return results
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(kwargs['bundle'].request)
    def obj_get(self, request=None, **kwargs):
        tenant = kwargs['bundle'].request.user.tenantlink.workspace
        res = Preference.for_tenant(tenant).objects.get(pk=kwargs['pk'])
        return res
    def rollback(self, bundles):
        pass

class ActivityResource(Resource):
    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')
    class Meta:
        resource_name = 'activity'
        object_class = Activity
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs
    def get_object_list(self, request):
        tenant = request.user.tenantlink.workspace
	user = Profile.for_tenant(tenant).objects.get(user=request.user)
        results = Activity.for_tenant(tenant).objects.all()
        return results
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(kwargs['bundle'].request)
    def obj_get(self, request=None, **kwargs):
        tenant = kwargs['bundle'].request.user.tenantlink.workspace
        res = Activity.for_tenant(tenant).objects.get(pk=kwargs['pk'])
        return res
    def rollback(self, bundles):
        pass

class RecordResource(Resource):
    id = fields.IntegerField(attribute='id')
    activity = fields.CharField(attribute='activity')
    start = fields.CharField(attribute='start_original')
    end = fields.CharField(attribute='end_original', null=True)
    class Meta:
        resource_name = 'record'
        object_class = Record
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs
    def get_object_list(self, request):
        tenant = request.user.tenantlink.workspace
	user = Profile.for_tenant(tenant).objects.get(user=request.user)
        results = Record.for_tenant(tenant).objects.filter(user=user)
        return results
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(kwargs['bundle'].request)
    def obj_get(self, request=None, **kwargs):
        tenant = kwargs['bundle'].request.user.tenantlink.workspace
        res = Record.for_tenant(tenant).objects.get(pk=kwargs['pk'])
        return res
    def rollback(self, bundles):
        pass

class CloseLastRecordResource(Resource):
    class Meta:
        resource_name = 'closelastrecord'
        object_class = Record
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['post']
    def obj_create(self, bundle, **kwargs):
	"""
	called for POST requests
	this fn only calls "new_task" with no activity
	in result, the current ongoing task is ended
	
	"""
        lazy_user = bundle.request.user
        tenant = lazy_user.tenantlink.workspace
	user = Profile.for_tenant(tenant).objects.get(user=lazy_user)
        activity = None
        new_task(user, activity)
    def rollback(self, bundles):
        pass

