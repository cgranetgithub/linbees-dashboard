from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource, ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from backapps.record.models import Record, new_task
from backapps.profile.models import Profile

class RecordResource(ModelResource):
    id = fields.IntegerField(attribute='id')
    task = fields.CharField(attribute='task')
    start = fields.CharField(attribute='start_original')
    end = fields.CharField(attribute='end_original', null=True)
    class Meta:
        resource_name = 'record'
        queryset = Record.objects.all()
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
    #def detail_uri_kwargs(self, bundle_or_obj):
        #kwargs = {}
        #if isinstance(bundle_or_obj, Bundle):
            #kwargs['pk'] = bundle_or_obj.obj.id
        #else:
            #kwargs['pk'] = bundle_or_obj.id
        #return kwargs
    def get_object_list(self, request):
        profile = request.user.profile
        tenant = profile.workspace
        #user = Profile.objects.by_workspace(tenant).get(user=request.user)
        results = Record.objects.by_workspace(tenant).filter(profile=profile)
        return results
    #def obj_get_list(self, request=None, **kwargs):
        #return self.get_object_list(kwargs['bundle'].request)
    #def obj_get(self, request=None, **kwargs):
        #tenant = kwargs['bundle'].request.user.profile.workspace
        #res = Record.objects.by_workspace(tenant).get(pk=kwargs['pk'])
        #return res
    #def rollback(self, bundles):
        #pass

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
        this fn only calls "new_task" with no task
        in result, the current ongoing task is ended
        
        """
        lazy_user = bundle.request.user
        profile = lazy_user.profile
        #tenant = lazy_user.profile.workspace
        #user = Profile.objects.by_workspace(tenant).get(user=lazy_user)
        task = None
        new_task(user, task)
    #def rollback(self, bundles):
        #pass

