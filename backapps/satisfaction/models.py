from django.db import models

class Criteria(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    updated_at  = models.DateTimeField(auto_now=True
					    , verbose_name=_('updated at'))
    name        = models.CharField(unique=True, max_length=255
					      , verbose_name=_('name'))
    description = models.CharField(max_length=255, blank=True
					      , verbose_name=_('description'))

class Satisfaction(TenantModel):
    """
    Inherits TenantModel => tenant specific class
    """
    is_active   = models.BooleanField(default=True
					    , verbose_name=_('active'))
    created_at  = models.DateTimeField(auto_now_add=True
					    , verbose_name=_('created at'))
    criteria    = models.ForeignKey(Criteria)
    user        = models.ForeignKey(Profile, editable=False)
