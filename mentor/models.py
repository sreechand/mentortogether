from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from mentortogether.user.models import MentorApplication, MenteeApplication

# --------------#
# Model Project #
# --------------#

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

# --------------------#
# Model WritingPrompt #
# --------------------#

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

# -----------------#
# Model Mentorship #
# -----------------#

class Mentorship(models.Model):
    project   = models.ForeignKey(Project, 
                                  unique=False, 
                                  blank=False)
    mentor_app= models.ForeignKey(MentorApplication, 
                                  unique=False,
                                  blank=False, 
                                  related_name="mentorship_mentor_app_set")
    mentee_app= models.ForeignKey(MenteeApplication, 
                                  unique=False, 
                                  blank=False, 
                                  related_name="mentorship_mentee_app_set")
    mentor_usr= models.ForeignKey(User, 
                                  editable=False,
                                  unique=False, 
                                  blank=False, 
                                  related_name="mentorship_mentor_set")
    mentee_usr= models.ForeignKey(User, 
                                  editable=False, 
                                  unique=False, 
                                  blank=False, 
                                  related_name="mentorship_mentee_set")

    def save(self):
        self.mentor_usr = self.mentor_app.user
        self.mentee_usr = self.mentee_app.user
        super(Mentorship,self).save()
    
# --------------#
# Model Message #
# --------------#

class MessageManager(models.Manager):
    def post(self, mentorship, sender, text):
        m = Message(mentorship=mentorship, sender=sender, text=text)
        m.save()
        return m

    def get_msgs_within(date1, date2):
        self.filter(senton__gte=date1, senton__lte=date2)

class Message(models.Model):
    mentorship= models.ForeignKey(Mentorship, blank=False, editable=False)
    sender    = models.ForeignKey(User, blank=False, editable=False, related_name="message_senders")
    senton    = models.DateTimeField(auto_now=True, editable=False)
    subject   = models.CharField(max_length=100, blank=True)
    text      = models.TextField(blank=True, verbose_name="Message")
    draft     = models.BooleanField(default=False, blank=True)
    objects   = MessageManager()

    def text_htmlize(self):
        return self.text.replace("\n", "<br>") 
