from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mentortogether.user.models import Photo
from mentortogether.user.models import MenteeApplication
import choices

class PhotoUploadForm(forms.ModelForm):
    """
    User photo upload form
    """
    def clean_image(self):
        from PIL import Image
        from mentortogether import settings
        import StringIO

        image = self.cleaned_data['image']

        # check content type 
        ct_main, ct_sub = image.content_type.split('/')
        if not (ct_main == 'image' and ct_sub in ['jpeg', 'gif', 'png']):
            raise forms.ValidationError(u'JPEG, PNG, GIF only.')

        if image.size > settings.USER_PHOTO_MAX_UPLOAD_SIZE:
            raise forms.ValidationError(u'Image is too big')

        try:
            img_obj = Image.open(StringIO.StringIO(image.read()))
        except Exception:
            raise forms.ValidationError(u'Invalid image file')    

        # check dimensions 
        width, height = img_obj.size

        if width > settings.USER_PHOTO_MAX_UPLOAD_WIDTH:
            raise forms.ValidationError(u"Maximum image width is %dpx"
                                        % settings.USER_PHOTO_MAX_UPLOAD_WIDTH)
        if height > settings.USER_PHOTO_MAX_UPLOAD_HEIGHT:
            raise forms.ValidationError(u"Maximum image height is %dpx"
                                        % settings.USER_PHOTO_MAX_UPLOAD_WIDTH)

        image.seek(0)       

        return image

    def save(self, user):
        photo = Photo.objects.upload(user=user, 
                                     image=self.cleaned_data['image'])

    class Meta:
        model  = Photo

class ApplicationForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        app = super(ApplicationForm,self).save(*args, **kwargs)

        if app.user is None:
            app.save()
            return app

        # update redundant information
        app.user.first_name = app.first_name
        app.user.last_name = app.last_name
        app.user.save()

        return app


class MentorApplicationForm(ApplicationForm):
    role = 'mentor'

    dob               = forms.DateField(label=u'Date of Birth',
                                        help_text=u'Format dd/mm/yyyy',
                                        required=True,
                                        input_formats=("%d/%m/%Y",))

    curr_occup_since  = forms.DateField(label=u'Current Occupation Held Since',
                                        help_text=u'Format mm/yyyy',
                                        input_formats=("%m/%Y",),
                                        required=True)
    class Meta:
        from mentortogether.user.models import MentorApplication
        model   = MentorApplication
        fields  = ( 'email', 
                    'first_name', 
                    'last_name', 
                    'gender', 
                    'dob',
                    'contact_no',
                    'curr_occup_title', 
                    'curr_occup_co', 
                    'curr_occup_func', 
                    'curr_occup_industry',
                    'curr_occup_since',
                    'prev_occup_title', 
                    'prev_occup_co', 
                    'prev_occup_func', 
                    'prev_occup_industry',
                    'edu_0_degree', 
                    'edu_0_major', 
                    'edu_0_univ',
                    'edu_1_degree', 
                    'edu_1_major', 
                    'edu_1_univ',
                    'edu_2_degree', 
                    'edu_2_major', 
                    'edu_2_univ',
                    'mentor_match_pref', 
                    'hobbies', 
                    'reference', 
                    'prev_ngo',
                    'bangalore' )
                          

class MenteeApplicationForm(ApplicationForm):
    """
    Mentee Application Form
    """
    role = 'mentee'
    dob = forms.DateField(
                label=u'Date of Birth',
                help_text=u'Format dd/mm/yyyy',
                required=True,
                input_formats=("%d/%m/%Y",))
    school = forms.ChoiceField(
                label="School/Institutions",
                required=True,
                choices=choices.SchoolChoices,
                help_text="Select the school/organization you belong to.")
    subjects = forms.CharField(
                label="Subjects",
                required=False,
                widget=forms.Textarea,
                help_text="List all the subjects in your current course")
    mentor_role1 = forms.ChoiceField(
                initial=choices.MentorRoleChoices[0][0],
                label='Mentor Role #1',
                required=True,
                choices=choices.MentorRoleChoices)
    mentor_role2 = forms.ChoiceField(
                initial=choices.MentorRoleChoices[1][0],
                label='Mentor Role #2',
                required=True,
                choices=choices.MentorRoleChoices)
    mentor_role3 = forms.ChoiceField(
                initial=choices.MentorRoleChoices[2][0],
                label='Mentor Role #3',
                required=True,
                choices=choices.MentorRoleChoices)
    mentor_role1_other = forms.CharField(
                label='', 
                required=False, 
                help_text='If Other, please specify.',
                max_length=128)
    mentor_role2_other = forms.CharField(
                label='', 
                required=False, 
                help_text='If Other, please specify.',
                max_length=128)
    mentor_role3_other = forms.CharField(
                label='', 
                required=False, 
                help_text='If Other, please specify.',
                max_length=128)
    languages = forms.MultipleChoiceField(
                required=True,
                choices=choices.LanguageChoices,
                help_text='Select all languages you speak. (Use Ctrl+Click to select multiple options.)')

    class Meta:
        model = MenteeApplication
        fields  = ( 'email', 'first_name', 'last_name', 'gender', 'dob', 
                    'school', 'grade', 'languages',
                    'preuniv_interest', 'puc_course', 'degree_course', 'subjects',
                    'career1', 'career2', 'career3', 'career4', 'career5',
                    'mentor_role1', 'mentor_role1_other', 
                    'mentor_role2', 'mentor_role2_other', 
                    'mentor_role3', 'mentor_role3_other', )

    def clean_languages(self):
        # For now, just store languages as a comman separated text blob. It
        # is unclear how this could be used in report generated in the future,
        # at which point such information could be in a ManyToManyField form.
        return ', '.join(self.cleaned_data['languages'])

    def clean(self):
        cleaned_data = self.cleaned_data
        mentor_role1 = cleaned_data.get("mentor_role1")
        mentor_role2 = cleaned_data.get("mentor_role2")
        mentor_role3 = cleaned_data.get("mentor_role3")

        # TODO:
        other_err_msg = u"Other selected, but not specified"
        if mentor_role1 == 'Other':
            other = cleaned_data["mentor_role1_other"]
            if not other:
                self._errors["mentor_role1_other"] = self.error_class([other_err_msg])
            else:
                cleaned_data["mentor_role1"] = cleaned_data["mentor_role1_other"]
        return cleaned_data

class MenteeApplicationForm_Part1(forms.ModelForm):
    class Meta:
        model = MenteeApplication
        fields = ( 'email', 'first_name', 'last_name', 'dob',
                   'grade', 'school' )


class RestrictedMentorApplicationForm(MentorApplicationForm):
    class Meta(MentorApplicationForm.Meta):
        # exclude email from changes
        exclude = ( 'email' )
        
class RestrictedMenteeApplicationForm(MenteeApplicationForm):
    class Meta(MenteeApplicationForm.Meta):
        # exclude email from changes
        exclude = ( 'email' )

def get_appform_factory(user, restricted=False):
    if user.get_profile().role == 'mentor':
        if restricted:
            return RestrictedMentorApplicationForm
        else:
            return MentorApplicationForm
    elif user.get_profile().role == 'mentee':
        if restricted:
            return RestrictedMenteeApplicationForm
        else:
            return MenteeApplicationForm
    else:
        assert "Bug." and False

def get_appform(user, data=None, initial=None):
    form_factory = get_appform_factory(user, restricted=True)
    return form_factory(data=data, 
                        initial=initial, 
                        instance=user.get_profile().get_app())
