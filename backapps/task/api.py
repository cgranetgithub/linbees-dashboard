#from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from backapps.task.models import Task
from backapps.profile.models import Profile

class TaskResource(ModelResource):
    #id = fields.IntegerField(attribute='id')
    #name = fields.CharField(attribute='name')
    class Meta:
        resource_name = 'task'
        queryset = Task.objects.all()
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
        tenant = request.user.profile.workspace
        #user = Profile.objects.by_workspace(tenant).get(user=request.user)
        results = Task.objects.by_workspace(tenant).all()
        return results
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(kwargs['bundle'].request)
    def obj_get(self, request=None, **kwargs):
        tenant = kwargs['bundle'].request.user.profile.workspace
        res = Task.objects.by_workspace(tenant).get(pk=kwargs['pk'])
        return res
    #def rollback(self, bundles):
        #pass