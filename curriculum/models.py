#
# copyright (c) 2010 Mentortogether
#
from django.db import models
from django.contrib.auth.models import User

class Curriculum(models.Model):
    """
    `Curriculum` represents a single curriculum document, 
    which is composed of many `CurriculumNode`s.
    """
    title       = models.CharField(max_length=128, blank=False)
    summary     = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)

    def get_active_sections(self):
        """
        Returns section objects that are active, ordered by rank.
        """
        return ( self.curriculumsection_set
                    .filter(is_active=True)
                        .order_by('rank') )

    def __unicode__(self):
        return self.title

class CurriculumSection(models.Model):
    """
    `CurriculumSection` represents a section in a curriculum.
    """
    curriculum  = models.ForeignKey(Curriculum, null=False)
    title       = models.CharField(max_length=128)
    summary     = models.TextField()
    rank        = models.IntegerField(default=1, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by   = models.ForeignKey(User, related_name='curriculumsection_creator_set', null=False)
    edit_date   = models.DateTimeField(auto_now=True)
    edit_by     = models.ForeignKey(User, related_name='curriculumsection_editor_set', null=False)
    is_active   = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def get_active_prompts(self):
        """
        Returns section objects that are active, ordered by rank.
        """
        return ( self.curriculumprompt_set
                    .filter(is_active=True)
                        .order_by('rank') )


class CurriculumPrompt(models.Model):
    """
    `CurriculumPrompt` represents a sigle writing prompt.
    """
    section     = models.ForeignKey(CurriculumSection, null=False)
    title       = models.CharField(max_length=128)
    summary     = models.TextField()
    mentor_doc  = models.TextField()
    mentee_doc  = models.TextField()
    rank        = models.IntegerField(default=1, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by   = models.ForeignKey(User, related_name='curriculumprompt_creator_set', null=False)
    edit_date   = models.DateTimeField(auto_now=True)
    edit_by     = models.ForeignKey(User, related_name='curriculumprompt_editor_set', null=False)
    is_active   = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title


