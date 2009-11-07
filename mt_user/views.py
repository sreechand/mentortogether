from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mentortogether.mt_user.forms import MTUserSignupForm
from mentortogether.mt_user.models import MTUser

# ./signup view
def signup(request, account_type=None):
    """
    The user/signup view
    """

    # if no account_type was given, render a selection page
    if account_type == None or not account_type in ( 'mentor', 'mentee' ):
        return render_to_response('signup/select_profile.html')

    error = False

    if request.method == 'POST':
        form = MTUserSignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render_to_response('signup/confirmation.html', 
                                        {'account_type' : new_user.account_type,
                                         'email' : new_user.email })
        else:
            error = True
    else:
        form = MTUserSignupForm(initial={'account_type' : account_type })

    return render_to_response('signup/signup.html', 
                                {'form' : form,
                                 'account_type' : account_type,
                                 'error': error})

def activate(request, key):
    """
    Activates a user account based on the activate key
    """
    activation_key = key
    user = MTUser.objects.activateAccount(activation_key)
    if user == False:
        return render_to_response('signup/invalid_activation.html',
                                 {'activation_key' : activation_key})
    else:
        return render_to_response('signup/activated.html', {'user' : user})

"""
def login(request):
        form = MTLoginSignupForm()
"""
