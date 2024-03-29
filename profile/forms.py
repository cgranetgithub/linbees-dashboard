from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from profile.models import Profile
from libs.messages import public_email_not_allowed, existing_email
from mptt.forms import TreeNodeChoiceField


EMAIL_PROVIDER_BLACKLIST = (

#Default domains included
"aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
"google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
"live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",

#Other global domains
"email.com", "games.com", "gmx.net", "hush.com", "hushmail.com", "inbox.com",
"lavabit.com", "love.com", "pobox.com", "rocketmail.com",
"safe-mail.net", "wow.com", "ygm.com", "ymail.com", "zoho.com",

#United States ISP domains
"bellsouth.net", "charter.net", "cox.net", "earthlink.net", "juno.com",

#British ISP domains
"btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk",
"ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk",
"virgin.net", "wanadoo.co.uk", "bt.com",

#Chinese ISP domains
"sina.com", "qq.com",

#French ISP domains
"hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr",
"sfr.fr", "neuf.fr", "free.fr"

#German ISP domains
"gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de",

#Russian ISP domains
"mail.ru", "rambler.ru", "yandex.ru",

#Belgian ISP domains
"hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be",

#Argentinian ISP domains
"hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar",

#Domains used in Mexico
'hotmail.com', 'gmail.com', 'yahoo.com.mx', 'live.com.mx', 'yahoo.com', 'hotmail.es',
'live.com', 'hotmail.com.mx', 'prodigy.net.mx', 'msn.com',
)

class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        self.cleaned_data['username'] = username.lower()
        return super(LoginForm, self).clean()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username',
                'password1', 'password2')
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'email' in self.cleaned_data:
            # email forced to lower case
            email = self.cleaned_data['email'].lower()
            self.cleaned_data['email'] = email
            #check email unicity
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(existing_email)
            #check non-public email domain
            provider = email.split('@')[1]
            if provider in EMAIL_PROVIDER_BLACKLIST:
                raise forms.ValidationError(
                                    public_email_not_allowed%{'domain':provider})
        if 'username' in self.cleaned_data:
            # email forced to lower case
            username = self.cleaned_data['username'].lower()
            self.cleaned_data['username'] = username
        # Always return the full collection of cleaned data.
        return cleaned_data
    def save(self, commit=True):
        user=super(RegistrationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        user.is_active = True
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    def __init__(self, ws, admin, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # me and my descendant tasks
        my_descendants = admin.profile.get_descendants(include_self=True)
        # he and his descendant
        his_descendants = []
        if self.instance is not None:
            his_descendants = self.instance.get_descendants(include_self=True)
            desc_ids = [ i.user for i in his_descendants ]
            my_descendants = my_descendants.exclude(user__in=desc_ids)
        # all except descendants
        #qs = Profile.objects.by_workspace(ws)
        #if self.instance is not None:
            #descendants = self.instance.get_descendants(include_self=True)
            #desc_ids = [ i.user for i in descendants ]
            #qs = qs.exclude(user__in=desc_ids)
        self.fields['parent'] = TreeNodeChoiceField(label=_('Manager'),
                                                    queryset=my_descendants,
                                                    required=False)
    class Meta:
        model = Profile
        #fields = ['start_date', 'end_date', 'daily_wage']
        exclude = ('workspace', 'user', 'has_accepted_terms', 'power_transfer',
                   'is_primary', 'department')
        
#class ProfileListForm(forms.Form):
    #plist = forms.MultipleChoiceField(label=_('Users')
                                    #, widget=forms.CheckboxSelectMultiple)
    #def __init__(self, ws, *args, **kwargs):
        #super(ProfileListForm, self).__init__(*args, **kwargs)
        #pl = Profile.objects.by_workspace(ws).filter()
        #self.fields['plist'].choices = ( (p.user.id, p.user.email) for p in pl )
        #self.fields['plist'].initial = [ p.user.id for p in pl ]
