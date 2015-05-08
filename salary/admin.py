from django.contrib import admin
#from models import DailySalary
from django.apps import apps

#admin.site.register(DailySalary)
admin.site.register(apps.get_model('salary', 'DailySalary'))

