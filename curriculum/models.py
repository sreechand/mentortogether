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
    title       = models.TextField(blank=False)
    summary     = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)


class CurriculumNode(models.Model):
    """
    `CurriculumNode` represents a single node in a two-level 
    curriculum system.
    """
    curriculum  = models.ForeignKey('Curriculum', null=False)
    title       = models.TextField()
    summary     = models.TextField()
    mentor_doc  = models.TextField()
    mentee_doc  = models.TextField()
    rank        = models.IntegerField(default=1, blank=False)
    section     = models.ForeignKey('self', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by   = models.ForeignKey(User, 
                                    related_name='curriculumnode_creator_set',
                                    null=False)
    edit_date   = models.DateTimeField(auto_now=True)
    edit_by     = models.ForeignKey(User, 
                                    related_name='curriculumnode_editor_set',
                                    null=False)
    is_section  = models.BooleanField(null=False)
    is_active   = models.BooleanField(default=True)
