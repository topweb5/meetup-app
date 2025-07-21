from django import forms
from .models import Participant, Meetup, myUser, Speaker
from django.contrib.auth.forms import UserCreationForm


#Register form
class MyUserRegistrationForm(UserCreationForm):
    class Meta:
        model=myUser
        fields= ['name', 'username', 'email', 'password1', 'password2','image' ]

class ParticipantForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['email']


class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields =['title', 'from_date',  'to_date', 'meetup_time', 'description', 'organizer_email',  'address', 'activate','image',]


class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields =['name', 'email','phone', 'bio', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = [ 'name', 'username', 'email', 'bio', 'image', 'mobile_number', 'birth_date',]