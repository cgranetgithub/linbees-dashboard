from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from apps.signup.forms import SignupForm

def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = authenticate(
                            username=user_form.cleaned_data["username"],
                            password=user_form.cleaned_data["password2"])
            if user is not None and user.is_active:
                login(request, user)
                name = user.first_name or user.username
                ws_name = user.profile.workspace.name
                messages.warning(request, _("%(name)s, your account was "
"successfully created. Welcome to %(ws)s dashboard!")%{'name':name
                                                    ,'ws':ws_name})
                return redirect(reverse('overview'))
    else:
        user_form = SignupForm()
    return render(request, 'signup/signup.html',
                { 'user_form': user_form,
                  'form_action': reverse("signup:signup")})
