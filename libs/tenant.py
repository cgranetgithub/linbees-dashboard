from django.db import models
#from django.db.models.query import QuerySet
#from model_utils.managers import PassThroughManager
from apps.workspace.models import Workspace
from django.core.exceptions import ValidationError

#class TenantQuerySet(QuerySet):
    #def by_workspace(self, ws):
        #return self.filter(workspace=ws)

class TenantModel(models.Model):
    workspace = models.ForeignKey(Workspace)
    msg = u'workspace is a mandatory argument'
    #objects = PassThroughManager.for_queryset_class(TenantQuerySet)()
    class Meta:
        abstract = True
    def get_or_create(defaults=None, **kwargs):
        if 'workspace' not in kwargs:
            raise ValidationError(msg)
        super(TenantModel, self).get_or_create(defaults=None, **kwargs)
    def filter(**kwargs):
        if 'workspace' not in kwargs:
            raise ValidationError(msg)
        super(TenantModel, self).filter(**kwargs)
    def create(**kwargs):
        if 'workspace' not in kwargs:
            raise ValidationError(msg)
        super(TenantModel, self).create(**kwargs)
    def get(**kwargs):
        if 'workspace' not in kwargs:
            raise ValidationError(msg)
        super(TenantModel, self).get(**kwargs)
    def exclude(**kwargs):
        if 'workspace' not in kwargs:
            raise ValidationError(msg)
        super(TenantModel, self).exclude(**kwargs)
