from forms import MessageForm
from django import forms
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from datetime import date
from django.template.loader import render_to_string
from models import WritingPrompt, Project, Mentorship, Message
from mentortogether.curriculum.models import CurriculumPrompt
from mentortogether.curriculum.models import CurriculumSection
from mentortogether.mentor.models import CurriculumLog
from mentortogether.mentor.models import MessageThread
from mentortogether.mentor.models import Message
import datetime

def get_mentorship(user1, user2):
    if user1.get_profile().is_mentor() and user2.get_profile().is_mentee():
        mentor_usr, mentee_usr = (user1, user2)
    elif user2.get_profile().is_mentor() and user1.get_profile().is_mentee():
        mentor_usr, mentee_usr = (user2, user1)
    else:
        raise Http404

    mobj = Mentorship.objects.filter(mentor=mentor_usr, 
                                     mentee=mentee_usr)
    if mobj.count() < 1:
        raise Http404 
    if mobj.count() != 1:
        assert False

    return mobj[0]


def get_mentorship_objects(user):
    if user.get_profile().is_mentor():
        mobjs = Mentorship.objects.filter(mentor=user)
    elif user.get_profile().is_mentee():
        mobjs = Mentorship.objects.filter(mentee=user)
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

def get_obj_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def get_active_prompt(mentorship):
    """
    Returns the active prompt for a given mentorship. Returns Non
    if none.
    """
    try:
        return CurriculumLog.objects.get(mentorship=mentorship, is_active=False)
    except:
        return None

def deactivate_prompt(prompt):
    prompt.is_active = False
    prompt.save()

def get_active_log_or_none(mentorship):
    """
    Returns an active prompt for a given `Mentorship`, if there exists
    one, or returns None.
    """
    try:
        return mentorship.curriculumlog_set.get(is_active=True)
    except CurriculumLog.DoesNotExist:
        return None

@login_required
def prompt_start(request, mid, pid):
    mentorship = get_object_or_404(Mentorship, pk=mid)
    if get_active_log_or_none(mentorship) is not None:
        request.user.message_set.create(message="You already have an active prompt!")
    else:
        prompt = get_object_or_404(CurriculumPrompt, pk=pid)
        CurriculumLog.objects.create(mentorship=mentorship, prompt=prompt, is_active=True)
    return redirect("prompt-listing", mid=mid)


@login_required
def prompt_stop(request, mid, pid):
    mentorship = get_object_or_404(Mentorship, pk=mid)
    log = get_active_log_or_none(mentorship)
    if log and log.prompt_id != int(pid):
        return Http404
    log.is_active = False;
    log.end_date = datetime.datetime.now()
    log.save()
    return redirect("prompt-listing", mid=mid)


def get_target_user(user, mentorship):
    if user.id == mentorship.mentor_id:
        return mentorship.mentee
    if user.id == mentorship.mentee_id:
        return mentorship.mentor
    raise Exception("bug")

def get_mentorship_context(request_user, mid):
    mentorship = get_object_or_404(Mentorship, pk=mid)
    target_user = get_target_user(request_user, mentorship)
    context = {}
    context['mentorship'] = mentorship
    context['target_user'] = target_user
    return context

@login_required
def thread_listing(request, mid):
    """
    List message threads for the given mentorship
    """
    context = get_mentorship_context(request.user, mid)
    template = 'mentor/thread_listing.html'
    mentorship = context['mentorship']
    context['threads'] = mentorship.messagethread_set.all().order_by('-timestamp')
    return render_to_response(template, context, RequestContext(request))


@login_required
def prompt_listing(request, mid):
    """
    List all available writing prompts for a given mentorship.
    Only a mentor can make such a selection.
    """
    
    # Only mentors can access this.
    if not request.user.get_profile().is_mentor():
        raise Http404

    mentorship = get_object_or_404(Mentorship, pk=mid)
    target_user = get_target_user(request.user, mentorship)
    context = {}
    template = 'mentor/prompt_select.html'
    context['mentorship'] = mentorship
    context['target_user'] = target_user

    # Collate bits of information about curriculum nodes, for the
    # given mentorship.
    nodes = []
    for section in mentorship.curriculum.get_active_sections():
        nodes.append({ 'section' : section })
        for prompt in section.get_active_prompts():
            log = get_obj_or_none(CurriculumLog, mentorship=mentorship, 
                                                 prompt=prompt,
                                                 is_active=True)
            nodes.append({ 'log' : log, 'prompt' : prompt })
    context['nodes'] = nodes

    return render_to_response(template, context, RequestContext(request))

@login_required
def view_thread(request, mid, tid):
    mentorship = get_object_or_404(Mentorship, pk=mid)
    thread     = get_object_or_404(MessageThread, pk=tid, mentorship=mentorship)
    messages   = Message.objects.filter(thread=thread).order_by('timestamp')

    return render_to_response('mentor/view_thread.html',
                              { 'mentorship'  : mentorship,
                                'thread'      : thread,
                                'thread_msgs' : messages },
                              context_instance=RequestContext(request))

@login_required
def post_message(request, mid, tid):
    if request.method != 'POST':
        raise Http404
    if ('text' not in request.POST) or (len(request.POST['text']) == 0):
        raise Http404
    mentorship = get_object_or_404(Mentorship, pk=mid)
    thread     = get_object_or_404(MessageThread, pk=tid, mentorship=mentorship)
    message    = Message.objects.create(thread=thread,
                                        sender=request.user,
                                        text=request.POST['text'])
    request.user.message_set.create(message="Message posted.")
    return redirect("view-thread", mid=mid, tid=thread.id)
        

@login_required
def new_thread(request, mid):
    mentorship = get_object_or_404(Mentorship, pk=mid)

    class NewMessageForm(forms.Form):
        subject = forms.CharField(label='Title', max_length=100, required=True)
        text    = forms.CharField(label='Message', widget=forms.Textarea, required=True)

        class Meta:
            fields = ('subject', 'text')

    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            # create a new thread object
            thread = MessageThread.objects.create(mentorship=mentorship,
                                                  subject=subject)
            # create the first message
            message = Message.objects.create(thread=thread,
                                             sender=request.user,
                                             text=text)
            return redirect("view-thread", mid=mid, tid=thread.id)
    else:
        form = NewMessageForm()

    return render_to_response('mentor/new_thread.html',
                              { 'mentorship' : mentorship,
                                'form'       : form },
                              context_instance=RequestContext(request))


@login_required
def mentorship(request, mid):

    mentorship  = get_object_or_404(Mentorship, pk=mid)
    target_user = get_target_user(request.user, mentorship)
    template    = "mentor/dashboard.html"
    context     = { 'target_user' : target_user,
                    'mentorship'  : mentorship }
    return render_to_response(template, context, RequestContext(request))
