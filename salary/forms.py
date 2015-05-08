from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory, BaseModelFormSet
#from models import DailySalary
from django.apps import apps

class SalaryForm(ModelForm):
    class Meta:
        #model = DailySalary
        model = apps.get_model('salary', 'DailySalary')
        fields = ['start_date', 'end_date', 'daily_wage']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

class BaseArticleFormSet(BaseModelFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        for form in self.forms:
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date > end_date:
                msg = u"End date connot be before start date"
                form.add_error('start_date', u"Start date must be lower than end date")
                form.add_error('end_date', u"End date must be greater than start date")

SalaryFormSet = modelformset_factory(
                        #DailySalary,
                        apps.get_model('salary', 'DailySalary'),
                        form=SalaryForm,
                        formset=BaseArticleFormSet,
                        fields=('start_date', 'end_date', 'daily_wage'),
                        extra=1,
                        )