from django.db import models
from django.core.exceptions import ValidationError

class TenantModel(models.Model):
    workspace = models.ForeignKey('workspace.Workspace')
    msg = u'workspace is a mandatory argument'
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
