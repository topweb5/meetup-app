from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns=[

path('', views.index, name='meetups'),
path('login/', views.loginPage, name='login'),
path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
path('register/', views.register, name='register'),
path('user-meeetups/<int:userId>', views.userMeeetups, name='user-meetups'),
path('meetup/<slug:slug>', views.meetup_details, name='meetup-details'),
path('meetup/participant-confirmation/', views.participant_connfirm, name='confirm-registration'),
path('meetup-update/<int:pk>', views.UpdateMeetup.as_view(), name='update-meetup'),
path('meetup-delete/<int:pk>', views.MeetupDelete.as_view(), name='delete-meetup'),
path('create-meetup/', views.MeetupsCreate.as_view(), name='create-meetup'),
#partipants
path('meetup-participants/<int:meetupid>', views.participants, name='meetup-participants'),

#speakers
path('add-speaker/<slug:meetup_slug>', views.add_speakers, name='add-speaker'),
path('meetup-speakers/<slug:meetup_slug>/<int:userid>', views.meetup_speakers, name='meetup-speakers'),
path('update-speaker/<int:pk>', views.SpeakerUpdate.as_view(), name='update-speaker'),
path('delete-speaker/<int:pk>', views.SpeakerDelete.as_view(), name='delete-speaker'),

##users
path('user-profile/<int:pk>', views.user_details, name='user-profile'),
path('update-user/', views.profile, name='update-user'),
]