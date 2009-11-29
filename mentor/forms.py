from django import forms
from models import Message

class MessageForm(forms.ModelForm):
    def save(self, user, mobj, wp):
        m = Message(mentorship=mobj, sender=user, text=self.cleaned_data['text'])
        m.save()
        return m
        
    class Meta:
        fields = [ 'text' ]
        model = Message
