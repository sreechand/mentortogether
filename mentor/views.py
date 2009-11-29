from models import WritingPrompt, Project, Mentorship, Message
from forms import MessageForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from datetime import date
from django.template.loader import render_to_string

def get_mentorship(user1, user2):
    if user1.get_profile().is_mentor() and user2.get_profile().is_mentee():
        mentor_usr, mentee_usr = (user1, user2)
    elif user2.get_profile().is_mentor() and user1.get_profile().is_mentee():
        mentor_usr, mentee_usr = (user2, user1)
    else:
        raise Http404

    mobj = Mentorship.objects.filter(mentor_usr=mentor_usr, 
                                     mentee_usr=mentee_usr)
    if mobj.count() < 1:
        raise Http404 
    if mobj.count() != 1:
        assert False

    return mobj[0]


def get_mentorship_objects(user):
    if user.get_profile().is_mentor():
        mobjs = Mentorship.objects.filter(mentor_usr=user)
    elif user.get_profile().is_mentee():
        mobjs = Mentorship.objects.filter(mentee_usr=user)
    else:
        raise Http404

    return mobjs


@login_required
def wp(request, username):

    # authorize mentor/mentee combination and get
    # mentorship object
    target_user = get_object_or_404(User, username=username)
    mobj = get_mentorship(request.user, target_user)

    # get writing prompt for today
    wp = mobj.project.writingprompt_set.get_prompt_by_date(date.today())
    if len(wp) != 1:
        raise Http404

    return render_to_response('mentorship_wp.html',
                              { 'wp' : wp[0],
                                'target_user' : target_user },
                              context_instance=RequestContext(request))

@login_required
def mentorship(request, username):

    target_user = get_object_or_404(User, username=username)

    # Get mentorship object for this user pair
    mobj = get_mentorship(request.user, target_user)

    # Get writing prompt
    wp = mobj.project.writingprompt_set.get_prompt_by_date(date.today())

    # TODO: check for when there are no writing prompts

    # Save posted message
    if request.method == 'POST':
        Message.objects.post(mobj, request.user, request.POST['message'])
        
    # Collect this weeks messages
    msgs = mobj.message_set.filter(senton__gte=wp[0].start_date).order_by('senton')

    msg_html = render_to_string('widgets/mentorship_msgset.html',
                                { 'msgs' : msgs,
                                  'start_date' : wp[0].start_date,
                                  'end_date'   : wp[0].end_date,
                                  'target_user': target_user },
                                context_instance=RequestContext(request))

    # Render messaging app
    return render_to_response('mentorship_msgs.html',
                              { 'wp' : wp[0], 
                                'msg_html' : msg_html,
                                'msgs' : msgs,
                                'target_user' : target_user },
                              context_instance=RequestContext(request))

