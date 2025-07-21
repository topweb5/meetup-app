from django.contrib import admin
from . models import myUser, Meetup, Participant, Speaker

# Register your models here.


class MeetupAdmin (admin.ModelAdmin):
   list_display=('title', 'organizer_email', 'city', 'address' )
   list_filter=('title',)
   prepopulated_fields={'slug':('title',)}
admin.site.register(myUser)
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Participant)
admin.site.register(Speaker)
