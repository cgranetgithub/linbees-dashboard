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
    def get_object_list(self, request):
        results = Task.objects.filter(workspace=request.user.profile.workspace)
        return results
