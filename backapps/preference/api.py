from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from backapps.profile.models import Profile
from backapps.preference.models import Preference

class PreferenceResource(ModelResource):
    #id = fields.IntegerField(attribute='id')
    #key = fields.CharField(attribute='key')
    #value = fields.CharField(attribute='value')
    class Meta:
        resource_name = 'preference'
        queryset = Preference.objects.all()
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
        results = Preference.objects.by_workspace(tenant
                                                  ).filter(profile=profile)
        return results
    #def obj_get_list(self, request=None, **kwargs):
        #return self.get_object_list(kwargs['bundle'].request)
    #def obj_get(self, request=None, **kwargs):
        #tenant = kwargs['bundle'].request.user.profile.workspace
        #res = Preference.objects.by_workspace(tenant).get(pk=kwargs['pk'])
        #return res
    #def rollback(self, bundles):
        #pass