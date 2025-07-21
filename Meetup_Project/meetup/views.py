from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meetup, Speaker, myUser, Participant
from django.db.models import Q
from . forms import ParticipantForm,MeetupForm, MyUserRegistrationForm, SpeakerForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from string import punctuation
# Create your views here.


#Login page
def loginPage(request):
    page='Login'
    if request.user.is_authenticated:
        return redirect('meetups')
    #when submit botton is pressed 
    if request.method=='POST':  
        email = request.POST.get('email')
        email.lower()
        password = request.POST.get('password')
        try:
            user=myUser.objects.get(email=email)  
        except:
            messages.error(request, 'User does not exist')
        user=authenticate(request, email=email, password=password)
        if user is not None:
          login(request, user)
          return redirect ('meetups')
        else:
          messages.error(request, 'Username OR password does not exit')
    context={'page':page}

    return render(request, 'meetup/login.html', context)

#Register
def register(request):
    page='Register'
    form=MyUserRegistrationForm()
    context={'form':form,  'page':page}

    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST,  request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email=user.email.lower()
            #email=user.email
            user.save()
            #send_mail('Thanks for registering','Thanks For Registering, we will get i touch with you soon..', settings.EMAIL_HOST_USER, [ email,])
            login(request, user)
            return redirect('meetups')
        else:
            messages.error(request, 'An error occurred during registration')
           
    return render(request, 'meetup/register.html',context )

def profile(request):
    page="Profile"
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={'form':form, 'page':page}
    return render(request, 'meetup/profile_form.html', context)



#User details
def user_details(request, pk):
    user=myUser.objects.get(id=pk)
    return render(request, 'meetup/user_details.html', {'user':user})
#Get all meetups
def index(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    meetups=Meetup.objects.filter(activate=True)
    meetups=meetups.order_by('-created_at')
    meetups=meetups.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)

    )
    count=meetups.count
    

    return render(request, 'meetup/index.html', {'meetups':meetups, 'count':count})


#Get users meetups
def userMeeetups(request, userId):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    meetups=Meetup.objects.filter(user=userId)
    meetups=meetups.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)

    )
    count=meetups.count

    return render(request, 'meetup/user_meetups.html', {'meetups':meetups, 'count':count})

#Get a single meetup
def meetup_details(request,slug):

    try:

        meetup=Meetup.objects.get(slug=slug)
        participants=meetup.participant.all
        speakers=meetup.meetup_speakers.all


        if request.method=='GET':
            participantReg=ParticipantForm()
        else:
            participantReg=ParticipantForm(request.POST)
            if participantReg.is_valid():
                participant=participantReg.save()
                meetup.participant.add(participant)
                return redirect('confirm-registration')
        contex={'meetup':meetup, 'meetp_found':True, 'form':participantReg, 'participants':participants, 'speakers':speakers}
        return render(request, 'meetup/meetup_details.html', contex)
    except Exception as exc:
         return render(request, 'meetup/meetup_details.html', {'meetup_found':False})


class UpdateMeetup(UpdateView):

    model=Meetup
    form_class=MeetupForm
    template_name='meetup/meetup_form.html'
    success_url=reverse_lazy('meetups')
    context_object_name ='meetup'


#Delete Meetups
class MeetupDelete(LoginRequiredMixin,DeleteView):
    model=Meetup
    context_object_name='meetup'
    template_name='meetup/delete_meetup.html'
    success_url=reverse_lazy('meetups')

class MeetupsCreate(LoginRequiredMixin,CreateView):
    model=Meetup
    form_class = MeetupForm
    #exclude=[]
    success_url=reverse_lazy('meetups')
    template_name='meetup/meetup_form.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        title=form.instance.title
        for i in punctuation:
            title=title.replace(i, ' ')
        for space in title:
            title=title.replace(' ', '-')
        form.instance.slug=title
        
        return super(MeetupsCreate, self).form_valid(form)
    
#Add speakers
def add_speakers(request, meetup_slug):
   # selected_meetup=Meetup.objects.get(slug=meetup_slug)
    try:
        selected_meetup=Meetup.objects.get(slug=meetup_slug)
        
        if request.method=='GET':
            add_speaker_form=SpeakerForm()
        else:
           
            add_speaker_form= SpeakerForm(request.POST, request.FILES)
            if add_speaker_form.is_valid():
                add_speaker_form.instance.user=request.user
                
                speaker=add_speaker_form.save(commit=False)
                add_speaker_form.instance.meetup_name=selected_meetup.title
                speaker=add_speaker_form.save()
                selected_meetup.meetup_speakers.add(speaker)
                return redirect('meetups')
              
        return render(request, 'meetup/add_speakers.html', {
         'meet_found':True,
         'meetup':selected_meetup,
         'page':False, 
         'form': add_speaker_form ,
         

          })    
   
    except Exception as exc:
        return render(request, 'meetups/add_speakers.html', {
         'meet_found':False,
         
     })

def participant_connfirm(request):
    return render(request, 'meetup/confirm_participant.html')


def participants(request, meetupid):
    meetup=Meetup.objects.get(id=meetupid)
    participants=meetup.participant.all()
    participants=participants.order_by('-id')
    count=participants.count()
    
    return render(request, 'meetup/participants.html', {'participants':participants, 'count':count, 'meetup':meetup} )


#speakers
def meetup_speakers(request, meetup_slug, userid):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    meetup=Meetup.objects.get(slug=meetup_slug) 
    user_speakers=meetup.meetup_speakers.all()
    # if request.method=='GET':
   
    speakers=user_speakers.filter(
        Q(name__icontains=q)|
        Q(meetup_name__icontains=q)
        
        ) 
    count=user_speakers.count()
    return render(request, 'meetup/user_speakers.html', {'speakers':speakers, 'count':count, 'meetup':meetup} )

#speakers update
class SpeakerUpdate(LoginRequiredMixin, UpdateView):
    model=Speaker
    form_class = SpeakerForm
    template_name='meetup/add_speakers.html'
    success_url=reverse_lazy('meetups')
    
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(SpeakerUpdate, self).form_valid(form)
    
#Delete Speakers
class SpeakerDelete(LoginRequiredMixin,DeleteView):
    model=Speaker
    context_object_name='speaker'
    template_name='meetup/delete_speaker.html'
    success_url=reverse_lazy('meetups')