from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from PIL import Image
from django.http import HttpResponse
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from mentortogether import settings
from django.core.files.uploadedfile import SimpleUploadedFile

import datetime
import random
import re
import hashlib
import choices
import os
import StringIO


def generateActivationKey(name):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt+name).hexdigest()


class UserProfileManager(models.Manager):
    """
    Site-wide User Profile Manager
    """
    def create(self, user, role):
        profile = UserProfile(user=user, role=role)
        profile.save()
        return profile

class UserProfile(models.Model):
    """
    Site-wide user profile
    """
    user           = models.ForeignKey(User, 
                                       unique=True, 
                                       editable=False)

    role           = models.CharField(max_length=12,
                                      blank=False,
                                      choices=choices.ROLE_CHOICES)

    objects        = UserProfileManager()
    
    def get_app(self):
        """
        Returns the user's application in the database
        """
        if self.role == 'mentor':
            return self.mentorapplication
        elif self.role == 'mentee':
            return self.menteeapplication
        else:
            assert False


class PhotoManager(models.Manager):

    def upload(self, user, image):
        try:
            photo = self.get(user=user)
        except Photo.DoesNotExist:
            photo = Photo(user=user)

        # save original image
        img = Image.open(StringIO.StringIO(image.read()))
        img_data = StringIO.StringIO()
        img.save(img_data, "JPEG")
        photo.image = SimpleUploadedFile('orig.jpg', img_data.getvalue())

        # save image resized for tags
        tn  = img.copy()
        tn.thumbnail(settings.USER_PHOTO_TN_TAG_SIZE, Image.ANTIALIAS)
        tn_data = StringIO.StringIO()
        tn.save(tn_data, "JPEG")
        photo.tn_tag = SimpleUploadedFile('tag.jpg', tn_data.getvalue())


        # save image resized for profile
        tn  = img.copy()
        tn.thumbnail(settings.USER_PHOTO_TN_PROFILE_SIZE, Image.ANTIALIAS)
        tn_data = StringIO.StringIO()
        tn.save(tn_data, "JPEG")
        photo.tn_profile = SimpleUploadedFile('profile.jpg', tn_data.getvalue())
        photo.save()

        return photo

    def setup_default(self, user, filename):
        return self.upload( user, SimpleUploadedFile(filename, open(filename).read()) )


def get_user_photo(user):
    try:
        return user.photo
    except Photo.DoesNotExist:
        role, gender = user.get_profile().role, user.get_profile().get_app().gender
        print role, gender
        if role == 'mentor':
            if gender == 'Male':
                return Photo.objects.setup_default(user, settings.USER_PHOTO_DEFAULT_MALE_MENTOR)    
            if gender == 'Female':
                return Photo.objects.setup_default(user, settings.USER_PHOTO_DEFAULT_FEMALE_MENTOR) 
        if role == 'mentee':
            if gender == 'Male':
                return Photo.objects.setup_default(user, settings.USER_PHOTO_DEFAULT_MALE_MENTEE)
            if gender == 'Female':
                return Photo.objects.setup_default(user, settings.USER_PHOTO_DEFAULT_FEMALE_MENTEE)    


class Photo(models.Model):
    """
    Every user can upload one photo, which will be used as their
    avatar throughout the website. This model represents the image
    thumbnail and other details.
    """

    storage = FileSystemStorage(location=settings.PHOTOS_LOCATION)

    # Fields 

    user        = models.OneToOneField(User, 
                                    unique=True,
                                    editable=False) 

    image       = models.ImageField(storage=storage, 
                                    blank=False,
                                    verbose_name="Profile Photo",
                                    help_text="Max. 500kb; JPG, PNG, or GIF",
                                    upload_to=(lambda i, f: os.path.join('user', str(i.user.id), f)))

    tn_profile  = models.ImageField(storage=storage,
                                    editable=False,
                                    blank=True, 
                                    upload_to=(lambda i, f: os.path.join('user', str(i.user.id), f)))

    tn_tag      = models.ImageField(storage=storage,
                                    editable=False,
                                    blank=True, 
                                    upload_to=(lambda i, f: os.path.join('user', str(i.user.id), f)))

    timestamp   = models.DateTimeField(auto_now=True, 
                                    auto_now_add=True, 
                                    editable=False)

    # override manager
    objects = PhotoManager()

    def to_http_response(self, type=''):
        try:
            if type == 'profile':
                imgfile = open(self.tn_profile.path, "rb")
            elif type == 'tag':
                imgfile = open(self.tn_tag.path, "rb")
            else:
                imgfile = open(self.image.path, "rb")
            return HttpResponse(imgfile.read(), mimetype="image/jpeg")
        except:
            raise Http404
    
class Application(models.Model):
    """
    User Application Base Model. Captures some of the common
    fields in both MentorApplication and MenteeApplication.
    """

    class Meta:
        abstract = True

    APPLICATION_STATUS = (
        ( u'pending.approval', u'Pending Approval' ),
        ( u'pending.activation', u'Pending Activation' ),
        ( u'active', u'Active' ),
        ( u'inactive', u'Inactive' )
    )

    user           = models.OneToOneField(User, null=True, editable=False)

    profile        = models.OneToOneField(UserProfile, null=True, editable=False)

    gender         = models.CharField(max_length=6, 
                                      blank=False,
                                      choices=choices.GENDER_CHOICES)

    dob            = models.DateField(blank=False, 
                                      verbose_name="Date of Birth")

    timestamp      = models.DateTimeField(auto_now=True, editable=False)

    role           = models.CharField(max_length=12,
                                      blank=False,
                                      choices=choices.ROLE_CHOICES)

    activation_key = models.CharField(max_length=40, 
                                      editable=False, 
                                      unique=False)

    status         = models.CharField(max_length=64, 
                                      editable=False, 
                                      unique=False, 
                                      default='pending.approval',
                                      choices=APPLICATION_STATUS)

    email          = models.EmailField(unique=True, blank=False)
   
    first_name     = models.CharField(max_length=32, blank=False)

    last_name      = models.CharField(max_length=32, blank=False)


    def approve(self):
        """
        Approves the application. This includes
        (1) Changing status to pending.activation.
        (2) Sending user an activation link
        """
        if self.status == 'pending.approval':
            self.status = 'pending.activation'
            self.activation_key = generateActivationKey(self.email)
        elif self.status == 'pending.activation':
            # resend approval notice
            pass
        else:
            return

        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()

        subject = u'Mentor Together Application Approved'  
        text    = render_to_string('user/approval_email.html',
                                   { 'activation_key' : self.activation_key,
                                     'first_name'     : self.first_name,
                                     'last_name'      : self.last_name,
                                     'site_name'      : current_site.name,
                                     'domain'         : current_site.domain })

        from django.core.mail import send_mail
        send_mail(subject, text, 'noreply@mentortogether.org', [self.email])

        self.save()

    def activate(self, user, profile):
        """
        Activates an application, marking its status active.
        """
        if self.status != 'pending.activation':
            return
        self.status = 'active'
        self.activation_key = ''
        self.user = user            # set user key
        self.profile = profile      # set profile key
        self.save()
        return



class MenteeApplication(Application):
    """
    Mentee Application Model
    """

    grade               = models.IntegerField(verbose_name="Grade", 
                                              choices=choices.GRADE_CHOICES)

    school              = models.CharField(max_length=64,
                                           verbose_name="School",
                                           choices=choices.SCHOOL_CHOICES)

    preuniv_interest    = models.CharField(max_length=64,
                                           verbose_name="Pre-University Interests",
                                           choices=choices.PREUNIV_DISCIPLINE_CHOICES)

    career1             = models.CharField(max_length=64,
                                           verbose_name="Career Interest (1)",
                                           choices=choices.CAREER_INTEREST_CHOICES)

    career2             = models.CharField(max_length=64,
                                           verbose_name="Career Interest (2)",
                                           choices=choices.CAREER_INTEREST_CHOICES)

    career3             = models.CharField(max_length=64,
                                           verbose_name="Career Interest (3)",
                                           choices=choices.CAREER_INTEREST_CHOICES)

    career4             = models.CharField(max_length=64,
                                           blank=True,
                                           verbose_name="Career Interest (4)",
                                           choices=choices.CAREER_INTEREST_CHOICES)

    career5             = models.CharField(max_length=64,
                                           blank=True,
                                           verbose_name="Career Interest (5)",
                                           choices=choices.CAREER_INTEREST_CHOICES)

    skill_resume_score  = models.IntegerField(verbose_name="Resume Writing Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    skill_pres_score    = models.IntegerField(verbose_name="Presentation Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    skill_essay_score   = models.IntegerField(verbose_name="Essay Writing Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    skill_comp_score    = models.IntegerField(verbose_name="Computer Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    skill_comm_score    = models.IntegerField(verbose_name="Communication Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    skill_neg_score     = models.IntegerField(verbose_name="Negotiation Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    mentor_eng_score    = models.IntegerField(verbose_name="Develop Mentee's English Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    skill_analy_score   = models.IntegerField(verbose_name="Analytical Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    mentor_comp_score   = models.IntegerField(verbose_name="Develop Mentee's Computer Skills",
                                              choices=choices.SKILL_SCORE_CHOICES )

    mentor_esteem_score = models.IntegerField(verbose_name="Develop Mentee's Self Esteem",
                                              choices=choices.SKILL_SCORE_CHOICES )

    mentor_part_score   = models.IntegerField(verbose_name="Encourage Mentee to participate more in class",
                                              choices=choices.SKILL_SCORE_CHOICES )

    mentor_acad_score   = models.IntegerField(verbose_name="Broaden Mentee's knowledge about further academic choices",
                                              choices=choices.SKILL_SCORE_CHOICES )

    mentor_career_score = models.IntegerField(verbose_name="Broaden Mentee's knowledge about career options",
                                              choices=choices.SKILL_SCORE_CHOICES )

    def get_normalized_date_fields(self):
        return { 'dob' : self.dob.strftime("%d/%m/%Y") }


class MentorApplication(Application):
    """
    Mentor Application Model
    """

    curr_occup_title    = models.CharField(max_length=64, 
                                           blank=False,
                                           verbose_name="Current Occupation Title")

    curr_occup_co       = models.CharField(max_length=64, 
                                           blank=False,
                                           verbose_name="Current Occupation Company Name")

    curr_occup_func     = models.CharField(max_length=64, 
                                           blank=False, 
                                           verbose_name="Current Occupation Functionality Area",
                                           help_text="The department you work in, or the one that comes closest.",
                                           choices=choices.OCCUPATION_FUNCTIONALITY_AREA_CHOICES)

    curr_occup_industry = models.CharField(max_length=64, 
                                           blank=False, 
                                           verbose_name="Current Occupation Industry",
                                           help_text="The industry sector your company belongs to.",
                                           choices=choices.OCCUPATION_INDUSTRY_CHOICES)

    curr_occup_since    = models.DateField(blank=False,
                                           verbose_name="Held Since",
                                           help_text="Date since you have held this position.")

    prev_occup_title    = models.CharField(max_length=64, 
                                           blank=True,
                                           verbose_name="Previous Occupation Title")

    prev_occup_co       = models.CharField(max_length=64, 
                                           blank=True,
                                           verbose_name="Previous Occupation Company Name")

    prev_occup_func     = models.CharField(max_length=64, 
                                           blank=True, 
                                           verbose_name="Previous Occupation Functionality Area",
                                           help_text="The department you worked in, or the one that comes closest.",
                                           choices=choices.OCCUPATION_FUNCTIONALITY_AREA_CHOICES)

    prev_occup_industry = models.CharField(max_length=64, 
                                           blank=True, 
                                           verbose_name="Previous Occupation Industry",
                                           help_text="The industry sector the company belonged to.",
                                           choices=choices.OCCUPATION_INDUSTRY_CHOICES)

    edu_0_degree        = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="Education(1) Degree",
                                           choices=choices.EDUCATION_DEGREE_CHOICES)

    edu_0_major         = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="Major",
                                           choices=choices.EDUCATION_MAJOR_CHOICES)

    edu_0_univ          = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="University")

    edu_1_degree        = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="Education(2) Degree",
                                           choices=choices.EDUCATION_DEGREE_CHOICES)

    edu_1_major         = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="Major",
                                           choices=choices.EDUCATION_MAJOR_CHOICES)

    edu_1_univ          = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="University")

    edu_2_degree        = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="Education(3) Degree",
                                           choices=choices.EDUCATION_DEGREE_CHOICES)

    edu_2_major         = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="Major",
                                           choices=choices.EDUCATION_MAJOR_CHOICES)

    edu_2_univ          = models.CharField(max_length=64,
                                           blank=True, 
                                           verbose_name="University")

    mentor_match_pref   = models.CharField(max_length=64,
                                           blank=False, 
                                           verbose_name="Mentor-matching preference.",
                                           choices=choices.MENTOR_MATCH_PREF_CHOICES)

    hobbies             = models.TextField(blank=True)

    reference           = models.TextField(blank=True,
                                           verbose_name="Tell us how you heard about Mentortogether?")

    bangalore           = models.BooleanField(blank=False, 
                                              verbose_name="Resident of Bangalore?")

    contact_no          = models.CharField(max_length=32,
                                           blank=True,
                                           verbose_name="Contact No.",
                                           default="")

    prev_ngo            = models.TextField(blank=True, 
                                           verbose_name="Tell us about your previous involvement in any NGO/Non-profit work.",
                                           default="")
                    

    def get_normalized_date_fields(self):
        return { 'dob' : self.dob.strftime("%d/%m/%Y"),
                 'curr_occup_since' : self.curr_occup_since.strftime("%d/%m/%Y") }

