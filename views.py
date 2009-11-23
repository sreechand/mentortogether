from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def homepage(request):
    if request.user.is_authenticated():
        from mentortogether import settings
        return redirect( settings.LOGIN_REDIRECT_URL )
    else:
        return render_to_response('page/homepage.html')    

@login_required
def dashboard(request):
    """
    User Dashboard View

    * The user is redirected to his/her dashboard, after logging-in.
    * Check if there are any incomplete field in his profile, and
      request him to fill the profil up.
    """ 
    return render_to_response('mt/dashboard.html')    

@login_required
def home(request):
    """
    User Dashboard View

    * The user is redirected to his/her dashboard, after logging-in.
    * Check if there are any incomplete field in his profile, and
      request him to fill the profil up.
    """ 
    return render_to_response('home.html', context_instance=RequestContext(request))    
