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
    def get_object_list(self, request):
        profile = request.user.profile
        tenant = profile.workspace
        results = Record.objects.by_workspace(tenant).filter(profile=profile)
        return results

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

