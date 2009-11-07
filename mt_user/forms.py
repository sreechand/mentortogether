from django import forms
from django.contrib.auth.forms import UserCreationForm
from mentortogether.mt_user.models import MTUser

class MTUserSignupForm(UserCreationForm):
    """
    Basic user signup form extends the UserCreationForm, adding
    first name, last name, and an account type
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True);
    account_type = forms.CharField(widget=forms.widgets.HiddenInput())

    def save(self):
        return MTUser.objects.openAccount(self.cleaned_data)

    class Meta:
        model = MTUser
        fields = [ 'account_type', 
                   'first_name', 
                   'last_name', 
                   'email', 
                   'username', 
                   'password1', 
                   'password2' ]
