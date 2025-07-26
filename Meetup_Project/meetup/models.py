from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class myUser(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to='users')
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=10, null=True)
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Participant(models.Model):
    email=models.EmailField(unique=False)
    name=models.CharField(max_length=50)
    image=models.ImageField()
    def __str__(self):
        return f'{self.name}-{self.email}'


class Speaker(models.Model):
    user=models.ForeignKey(myUser,  on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200, null=True, blank=True)
    phone=models.CharField(max_length=200,null=True, blank=True)
    meetup_name=models.CharField(max_length=200,  null=True, blank=True)
    image=models.ImageField(upload_to='speaker_images')
    bio=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name


class Meetup(models.Model):
      user=models.ForeignKey(myUser,  on_delete=models.CASCADE, null=True, blank=True)
      organizer_email=models.EmailField(max_length=254, null=True)
      title=models.CharField(max_length=500)
      slug=models.SlugField(unique=True)
      description=models.TextField()
      image=models.ImageField(upload_to='meetups')
      city=models.CharField(max_length=50,  null=True, blank=True)
      address=models.TextField( null=True, blank=True)
      participant=models.ManyToManyField(Participant, blank=True)
      meetup_speakers=models.ManyToManyField(Speaker, blank=True )
      activate=models.BooleanField(default=True)
      created_at=models.DateTimeField(auto_now_add=True)
      meetup_date=models.DateField(blank=True, null=True)
      meetup_time=models.TimeField()
      from_date=models.DateField()
      to_date=models.DateField()

     
      def __str__(self):
        return f'{self.title} - {self.organizer_email}'
        

