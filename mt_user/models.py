from django.db import models
from django.contrib import auth
import datetime
import random
import re
import hashlib

class MTUser(auth.models.User):
    AC_STATE_CHOICES = (
        ( u'Activation', u'Activation' ),
        ( u'Pending', u'Pending' ),
        ( u'Approved', u'Approved' ),
        ( u'Banned', u'Banned' )
    )

    activation_key = models.CharField(max_length=40)
    account_state = models.CharField('pending', choices=AC_STATE_CHOICES, max_length=12)

class MTProfileManager(models.Manager):
    def openAccount(self, username, password, email):
        """
        stage 1: of user signup: open an account placeholder
        and generate and activation key and send it out to the
        user, for confirmation.
        """
        user = MTUser.objects.create_user\
                    (username=username, 
                     email=email, 
                     password=password)
        user.is_active = false;
        user.account_state = 'Activation'
        user.save()

        # Create a SHA1 hash as activation key for the new user.
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+user.username).hexdigest()
        profile = self.create(user=user, activation_key=activation_key)

#
# A generic profile class - This class is intended
# to be subclassed
#
class MTProfile(models.Model):
    GENDER_CHOICES = (
        ( u'Male', u'Male' ),
        ( u'Female', u'Female' ),
    )
    ROLE_CHOICES = (
        ( 0, u'Mentor' ),
        ( 1, u'Mentee' ),
        ( 2, u'Subscriber' )
    )
    user = models.ForeignKey(MTUser, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    role = models.IntegerField(choices=ROLE_CHOICES)
    age = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % ( self.user.first_name, self.user.last_name )

class MTProfileMentor(MTProfile):
    YESNO_CHOICES = (
        ( u'Yes', u'Yes' ),
        ( u'No', u'No' )
    )
    occupation = models.CharField(max_length=128)
