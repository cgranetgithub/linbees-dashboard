from django.forms import ModelForm
from django.forms.models import modelformset_factory
from models import DailySalary

class SalaryForm(ModelForm):
    class Meta:
        model = DailySalary
        fields = ['start_date', 'end_date', 'daily_wage']

SalaryFormSet = modelformset_factory(
                        DailySalary,
                        fields=('start_date', 'end_date', 'daily_wage'),
                        extra=0)