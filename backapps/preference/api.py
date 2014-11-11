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
    def get_object_list(self, request):
        profile = request.user.profile
        tenant = profile.workspace
        results = Preference.objects.by_workspace(tenant
                                                  ).filter(profile=profile)
        return results
