from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    """
    Notice model implements blobs of texts identified by
    a board to which it belongs.
    """
    BOARD_CHOICES = ( ('mentor-dashboard', 'Mentor Dashboard'),
                      ('mentee-dashboard', 'Mentee Dashboard') )

    board       = models.CharField(max_length=32, db_index=True, choices=BOARD_CHOICES)
    notice_text = models.TextField(blank=True, null=True)
    created_by  = models.ForeignKey(User, related_name="notice_creator_set")
    created_on  = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name="notice_modifier_set")
    modified_on = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        ordering = ['-modified_on', '-created_on']
