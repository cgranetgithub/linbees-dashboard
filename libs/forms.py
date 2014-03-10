from django import forms

class SelectForm(forms.Form):
    def __init__(self, request, choices, *args, **kwargs):
        if request.method == 'POST':
            super(SelectForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(SelectForm, self).__init__(*args, **kwargs)
        self.fields['ulist'] = forms.ChoiceField(
	    widget=forms.RadioSelect(attrs={'onchange':'this.form.submit()'}),
	    choices=choices, *args, **kwargs)

#class SelectMultipleForm(forms.Form):
      #def __init__(self, request, choices, label, *args, **kwargs):
        #if request.method == 'POST':
            #super(SelectMultipleForm, self).__init__(request.POST, *args, **kwargs)
        #else:
            #super(SelectMultipleForm, self).__init__(*args, **kwargs)
        #self.fields['ulist'] = forms.MultipleChoiceField(
					  #widget=forms.CheckboxSelectMultiple,
					  #choices=choices, label=label,
					  #*args, **kwargs)
