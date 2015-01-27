from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from apps.profile.models import Profile
from apps.preference.models import Preference

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
        results = Preference.objects.filter(profile=profile,
                                            workspace=profile.workspace)
        return results
