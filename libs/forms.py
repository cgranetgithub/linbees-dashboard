from django import forms

class SelectForm(forms.Form):
    def __init__(self, request, choices, *args, **kwargs):
        if request.method == 'POST':
            super(SelectForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(SelectForm, self).__init__(*args, **kwargs)
        self.fields['ulist'] = forms.ChoiceField(
	    widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit()'}),
	    choices=choices, *args, **kwargs)
