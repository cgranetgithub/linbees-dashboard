#from django import forms
#from django.forms.models import modelformset_factory
##from django.forms.formsets import BaseModelFormSet
#from django.forms.models import BaseModelFormSet
#from django.utils.translation import ugettext, ugettext_lazy as _
#from backapps.salary.models import FixedSalary

#class FixedSalaryForm(forms.ModelForm):
    #class Meta:
        #model = FixedSalary
	#fields = ('start_date', 'end_date', 'monthly_wage')

#class BaseFixedSalaryFormSet(BaseModelFormSet):
    #def clean(self):
	#"""Checks that records don't have overlapping dates."""
        #if any(self.errors):
            ## Don't bother validating the formset unless each form is valid on its own
            #return
	#super(BaseFixedSalaryFormSet, self).clean()
	#periods = []
        #for form in self.forms:
	    #if ('start_date' not in form.cleaned_data or 
		#'end_date'   not in form.cleaned_data   ):
		#continue
	    #start = form.cleaned_data['start_date']
	    #end   = form.cleaned_data['end_date']
	    ## check start <= end
	    #if not ( start <= end ):
		#raise forms.ValidationError(_("start date must be lower than end date"))
	    ## check no overlapping
	    #for p in periods:
		#if not ( (start <= end < p[0]) or (p[1] < start <= end) ):
		    #raise forms.ValidationError(_("overlapping dates detected"))
	    #periods.append([start, end])

#FixedSalaryFormSet = modelformset_factory(FixedSalary, formset=BaseFixedSalaryFormSet)
