from django.apps import AppConfig

class RecordConfig(AppConfig):
    name = 'record'
    verbose_name = "Record"
    
    def ready(self):
        import receivers
