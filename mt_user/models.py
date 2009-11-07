from django.db import models
from django.contrib import auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
import datetime
import random
import re
import hashlib

class MTUserManager(auth.models.UserManager):
    """ 
    Manager for User objects
    """ 
    def openAccount(self, user_info):
        """
        stage 1: of user signup: open an account placeholder,
        generate an activation key and send it out to the
        user, for confirmation.
        """
        user = self.create_user(
                     username=user_info['username'], 
                     email=user_info['email'], 
                     password=user_info['password2'])
        user.first_name = user_info['first_name']
        user.last_name = user_info['last_name']
        user.is_active = False;
        user.account_state = 'Activation'
        user.account_type = user_info['account_type']

        # Create a SHA1 hash as activation key for the new user.
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        user.activation_key = hashlib.sha1(salt+user.username).hexdigest()

        # Save to DB
        user.save()

        # Email the activation key to the user
        subject = render_to_string('signup/signup_activation_email_subject.txt')
        subject = ''.join(subject.splitlines()) # remove newlines
        message = render_to_string('signup/signup_activation_email_message.txt',
                                   {'activation_key' : user.activation_key,
                                    'first_name'     : user.first_name,
                                    'last_name'      : user.last_name })

        send_mail(subject, message, 'noreply@mentortogether.org', [user.email])

        return user

    def activateAccount(self, activation_key):
        """
        Activates a user account based on activation key.
        """
        try:
            user = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False
        user.is_active = True 
        user.account_state = 'Active'
        user.activation_key = 'ACTIVE'
        user.save()
        return user


class MTUser(auth.models.User):
    AC_STATE_CHOICES = (
        ( u'Activation', u'Activation' ),
        ( u'Pending', u'Pending' ),
        ( u'Approved', u'Approved' ),
        ( u'Banned', u'Banned' )
    )

    AC_TYPE_CHOICES = (
        ( u'mentor', u'mentor' ),
        ( u'mentee', u'mentee' ),
        ( u'subscriber', u'subscriber' )
    )

    account_type = models.CharField(max_length=12, choices=AC_TYPE_CHOICES)
    activation_key = models.CharField(max_length=40, unique=False)
    account_state = models.CharField('pending', choices=AC_STATE_CHOICES, max_length=12)

    objects = MTUserManager()

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
