from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import choices


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
                    'bangalore' )
                                        
class MenteeApplicationForm(ApplicationForm):
    role = 'mentee'

    dob = forms.DateField(label=u'Date of Birth',
                          help_text=u'Format dd/mm/yyyy',
                          required=True,
                          input_formats=("%d/%m/%Y",))
    class Meta:
        from mentortogether.user.models import MenteeApplication
        model   = MenteeApplication
        fields  = ( 'email', 
                    'first_name', 
                    'last_name', 
                    'gender', 
                    'dob',
                    'grade', 
                    'school', 
                    'preuniv_interest', 
                    'career1',
                    'career2', 
                    'career3', 
                    'career4', 
                    'career5',
                    'skill_resume_score', 
                    'skill_pres_score', 
                    'skill_essay_score',
                    'skill_comp_score', 
                    'skill_comm_score', 
                    'skill_neg_score',
                    'skill_analy_score', 
                    'mentor_comp_score', 
                    'mentor_esteem_score',
                    'mentor_eng_score',
                    'mentor_part_score', 
                    'mentor_acad_score', 
                    'mentor_career_score' )

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
