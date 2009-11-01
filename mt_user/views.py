from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'first_name', 'last_name' ]

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()

    return render_to_response('signup/signup.html', {'form' : form})
