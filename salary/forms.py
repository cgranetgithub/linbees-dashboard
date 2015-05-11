from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext, ugettext_lazy as _
from models import DailySalary
#from django.apps import apps

class SalaryForm(ModelForm):
    class Meta:
        model = DailySalary
        #model = apps.get_model('salary', 'DailySalary')
        fields = ['start_date', 'end_date', 'daily_wage']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
    def clean(self):
        cleaned_data = super(SalaryForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and (start_date > end_date):
            self.add_error('start_date', _('Start date should be lower than end date.'))
            self.add_error('end_date', _('End date should be greater than start date.'))

class BaseSalaryFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        # check no dates overlap
        for form in self.forms:
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date and end_date:
                index = self.forms.index(form) + 1
                for i in self.forms[index:]:
                    sd = i.cleaned_data.get("start_date")
                    ed = i.cleaned_data.get("end_date")
                    if (sd and ed) and (
                                ((sd >= start_date) and (sd <= end_date))
                                or ((ed >= start_date) and (ed <= end_date))
                                or ((sd <= start_date) and (ed >= end_date)) ):
                        msg = _('This period overlaps another one')
                        form.add_error('start_date', msg)
                        form.add_error('end_date', msg)
                        i.add_error('start_date', msg)
                        i.add_error('end_date', msg)

SalaryFormSet = modelformset_factory(
                        DailySalary,
                        #apps.get_model('salary', 'DailySalary'),
                        form=SalaryForm,
                        formset=BaseSalaryFormSet,
                        )