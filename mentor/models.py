from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from mentortogether.user.models import MentorApplication, MenteeApplication
from mentortogether.curriculum.models import Curriculum, CurriculumSection, CurriculumPrompt

class Project(models.Model):
    """
    Project Model
    """
    name            = models.CharField(max_length=32, blank=False)
    start_date      = models.DateField(blank=False)
    end_date        = models.DateField(blank=False)
    description     = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class WritingPromptManager(models.Manager):
    def get_prompt_by_date(self, date):
        return self.filter(start_date__lte=date, end_date__gte=date)

class WritingPrompt(models.Model):
    """
    This model defines the set of writing prompts presented to
    mentors and mentees, within a time period. Mentors and 
    mentees have different prompts.
    """
    project         = models.ForeignKey(Project, 
                                       unique=False, 
                                       blank=False)
    title           = models.CharField(max_length=64)
    mentor_prompt   = models.TextField(blank=True)
    mentee_prompt   = models.TextField(blank=True)
    start_date      = models.DateField(blank=False, 
                                       unique=True)
    end_date        = models.DateField(blank=False, 
                                       unique=True)

    objects = WritingPromptManager()

    def __str__(self):
        return self.title

class Mentorship(models.Model):
    """
    `Mentorship` represents a Mentor-Mentee pair in the system. Each
    pair is associated with a project and a curriculum.
    """
    project    = models.ForeignKey(Project, editable=True, blank=False)
    curriculum = models.ForeignKey(Curriculum, editable=True)
    mentor     = models.ForeignKey(User, editable=True, related_name="mentorship_mentor_set")
    mentee     = models.ForeignKey(User, editable=True, related_name="mentorship_mentee_set")

    def __str__(self):
        return ("mentor: %s <-> mentee: %s" 
                    % (self.mentor.get_full_name(), 
                        self.mentee.get_full_name()))

class MessageThread(models.Model):
    """
    Message thread object, which is a set of message objects.
    """
    mentorship = models.ForeignKey(Mentorship, blank=False, editable=False)
    subject    = models.CharField(max_length=100, blank=True, editable=False)
    timestamp  = models.DateTimeField(auto_now_add=True, auto_now=True)
    prompt     = models.ForeignKey(CurriculumPrompt, null=True, blank=True)


class Message(models.Model):
    """
    Message object.
    """
    thread     = models.ForeignKey(MessageThread, null=False)
    sender     = models.ForeignKey(User, null=False, blank=False,
                                   related_name="sender_set")
    timestamp  = models.DateTimeField(auto_now_add=True, auto_now=True)
    text       = models.TextField()
    is_draft   = models.BooleanField(default=False, blank=True)
    is_unread  = models.BooleanField(default=True)


class CurriculumLog(models.Model):
    """
    A log of curriculum activity for a given `mentorship`.
    """
    prompt     = models.ForeignKey(CurriculumPrompt, blank=False)
    mentorship = models.ForeignKey(Mentorship, blank=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date   = models.DateTimeField(null=True, blank=True)
    remarks    = models.TextField(blank=True, null=True)
    is_active  = models.BooleanField(blank=False, null=False)

