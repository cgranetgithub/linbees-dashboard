from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from backapps.workspace.models import Workspace

class TenantQuerySet(QuerySet):
    def by_workspace(self, ws):
        return self.filter(workspace=ws)

class TenantModel(models.Model):
    workspace = models.ForeignKey(Workspace)
    objects = PassThroughManager.for_queryset_class(TenantQuerySet)()
    class Meta:
        abstract = True
