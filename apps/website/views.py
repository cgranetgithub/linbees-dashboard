from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from apps.website.forms import ContactForm

def home(request):
    return render(request, 'website/home.html')

def dashboard(request):
    return render(request, 'website/dashboard.html')

def pricing(request):
    return render(request, 'website/pricing.html', {'price':settings.DEFAULT_PRICE})

def apps(request):
    return render(request, 'website/apps.html')

def about(request):
    return render(request, 'website/about.html')

def legal(request):
    return render(request, 'website/legal.html')

class ContactView(FormView):
    template_name = 'website/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('website:home')
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)

class BlankView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('connected!')

#def contact(request):
    #if request.method == 'POST': # If the form has been submitted...
        #form = ContactForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            #subject = form.cleaned_data['subject']
            #message = form.cleaned_data['message']
            #sender = form.cleaned_data['your_email']
            #recipients = ['c.granet@gmail.com']
            #send_mail(subject, message, sender, recipients)
            #return redirect(reverse('website:home')) # Redirect after POST
    #else:
        #form = ContactForm() # An unbound form
    #return render(request, 'website/contact.html', {
        #'form' : form,
        #'form_action' : reverse('website:contact'),
    #})
