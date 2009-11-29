from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from mentortogether.mentor.views import get_mentorship_objects

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
    """ 
    mobjs = get_mentorship_objects(request.user)
    if len( mobjs ) > 0:
        target_users = []
        if request.user.get_profile().is_mentor():
            for m in mobjs:
                target_users.append(m.mentee_usr)
        elif request.user.get_profile().is_mentee():
            for m in mobjs:
                target_users.append(m.mentor_usr)
    else:
        target_users = None

    return render_to_response('home.html', 
                              { 'target_users' : target_users },
                              context_instance=RequestContext(request))    
