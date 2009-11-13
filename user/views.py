from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def validateActivationKey(key):
    from mentortogether.user.models import MentorApplication
    from mentortogether.user.models import MenteeApplication

    try:
        app = MentorApplication.objects.get(activation_key=key)
        if app.status == 'pending.activation': return app
    except MentorApplication.DoesNotExist:
        pass

    try:
        app = MenteeApplication.objects.get(activation_key=key)
        if app.status == 'pending.activation': return app
    except MenteeApplication.DoesNotExist:
        pass

def activate(request, key):
    # Validate the activation key, and fetch the
    # associated application
    app = validateActivationKey(key)
    if app is None:
        return render_to_response('user/invalid_activation.html',
                                  { 'activation_key' : key })

    error = False
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create a new User object
            user = form.save(commit=False)
            user.email = app.email
            user.first_name = app.first_name
            user.last_name = app.last_name
            user.save() 
           
            # Create a site-wide profile for this User
            from models import UserProfile
            profile = UserProfile.objects.create(user, app.role)

            # Activate the application
            app.activate(user, profile)
 
            return render_to_response('user/signup_done.html')
        else:
            error = True
    else:    
        form = UserCreationForm()
    
    # Render a signup form     
    return render_to_response('user/signup.html',
                              { 'activation_key' : key,
                                'app' : app, 
                                'form': form })


def applicationForm(request, form_factory):
    error = False
    if request.method == 'POST':
        form = form_factory(request.POST)
        if form.is_valid():
            # Form is valid, create a new application object
            # and set its status to 'pending.approval'
            app = form.save(commit=False)
            app.role = form.role
            app.status = 'pending.approval'
            app.save()
            return render_to_response('user/application_submitted.html',
                                      { 'app' : app,
                                        'type': form_factory.role })
        else:
            error = True
    else:
        form = form_factory()

    return render_to_response('user/application_form.html',
                              { 'form' : form,
                                'type' : form_factory.role })


def apply(request, role):
    if role == 'mentor':
        from mentortogether.user.forms import MentorApplicationForm
        return applicationForm(request, MentorApplicationForm)
    elif role == 'mentee':
        from mentortogether.user.forms import MenteeApplicationForm
        return applicationForm(request, MenteeApplicationForm)
    else:
        return render_to_response('user/apply.html')
   

@login_required
def upage(request): 
    return render_to_response('user/dashboard.html', 
                              context_instance=RequestContext(request))

def get_appform_factory(user):
    if user.get_profile().role == 'mentor':
        from mentortogether.user.forms import MentorApplicationForm
        return MentorApplicationForm
    elif user.get_profile().role == 'mentee':
        from menteetogether.user.forms import MenteeApplicationForm
        return MenteeApplicationForm
    else:
        assert "Bug." and False

@login_required
def profile(request, action):
    from forms import get_appform, get_appform_factory
    error = False
    if request.method == 'POST':
        form = get_appform(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
        else:
            error = True
    else:
        initial = request.user.get_profile().get_app().get_normalized_date_fields()
        form = get_appform(user=request.user, initial=initial)

    return render_to_response('user/profile.html', 
                              { 'form' : form },
                              context_instance=RequestContext(request))
    return
