from forms import MessageForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from datetime import date
from django.template.loader import render_to_string
from models import WritingPrompt, Project, Mentorship, Message
from models import DraftText

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
def archive_index(request, username):
 
    target_user = get_object_or_404(User, username=username)

    # Get mentorship object for this user pair
    mobj = get_mentorship(request.user, target_user)

    wps = mobj.project.writingprompt_set.all().order_by('-start_date')

    return render_to_response('mentorship_archive_index.html',
                              { 'wps' : wps, 
                                'target_user' : target_user },
                              context_instance=RequestContext(request))

@login_required
def archive(request, username, yyyy, mm, dd):
    target_user = get_object_or_404(User, username=username)

    # Get mentorship object for this user pair
    mobj = get_mentorship(request.user, target_user)

    archive_date = date(int(yyyy), int(mm), int(dd)) 

    # Get writing prompt
    wp = mobj.project.writingprompt_set.get_prompt_by_date(archive_date)

    # Collect this weeks messages
    msgs = mobj.message_set.filter(senton__gte=wp[0].start_date)\
                .filter(senton__lte=wp[0].end_date).order_by('senton')

    msg_html = render_to_string('widgets/mentorship_msgset.html',
                                { 'msgs' : msgs,
                                  'start_date' : wp[0].start_date,
                                  'end_date'   : wp[0].end_date,
                                  'target_user': target_user })
    
    # Render messaging app
    return render_to_response('mentorship_archive.html',
                              { 'wp' : wp[0], 
                                'msg_html' : msg_html,
                                'target_user' : target_user },
                              context_instance=RequestContext(request))

@login_required
def mentorship(request, username):

    target_user = get_object_or_404(User, username=username)

    # Get mentorship object for this user pair
    mobj = get_mentorship(request.user, target_user)

    # Get writing prompt
    wp = mobj.project.writingprompt_set.get_prompt_by_date(date.today())

    # get draft text (or create object if it doesn't exist)
    try:
        drafts = request.user.send_drafttext_set.filter(recipient=target_user)
        if len(drafts) == 0:
            raise DraftText.DoesNotExist
        draft = drafts[0]
    except DraftText.DoesNotExist:
        draft = DraftText(sender=request.user, 
                          recipient=target_user, 
                          text='')

    # Save posted message
    if request.method == 'POST':
        if request.POST['formaction'] == "Save":
            draft.text = request.POST['message']
            draft.save()
            request.user.message_set.create(message="Message draft saved.")
        else:
            draft.text = ''
            draft.save()
            Message.objects.post(mobj, request.user, request.POST['message'])
        draft.save()
 
    # Collect this weeks messages
    msgs = mobj.message_set.filter(senton__gte=wp[0].start_date).order_by('senton')

    msg_html = render_to_string('widgets/mentorship_msgset.html',
                                { 'msgs' : msgs,
                                  'start_date' : wp[0].start_date,
                                  'end_date'   : wp[0].end_date,
                                  'target_user': target_user })

    # Render messaging app
    return render_to_response('mentorship_msgs.html',
                              { 'wp' : wp[0], 
                                'msg_html' : msg_html,
                                'msgs' : msgs,
                                'initial_text' : draft.text,
                                'target_user' : target_user },
                              context_instance=RequestContext(request))

