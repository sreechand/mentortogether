from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def homepage(request):
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
