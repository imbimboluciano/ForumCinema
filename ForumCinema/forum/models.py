from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import secrets



# Create your models here.
class Citazione(models.Model):
    descrizione = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.descrizione

class Movie(models.Model):
    titolo = models.CharField(max_length=200)
    anno = models.CharField(max_length=200)
    poster = models.CharField(max_length=500, default="CIao")

    def __str__(self) -> str:
        return self.titolo + " " + self.anno

class Avatar(models.Model):
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.image
    


class Review(models.Model):
    movie = models.ForeignKey(Movie,on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    descrizione = models.CharField(max_length=500)
    likes = models.ManyToManyField(User, related_name='review_like')
    date_published = models.DateField()

    def number_of_likes(self):
        return self.likes.count()
    

class Comment(models.Model):
    descrizione = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    review = models.ForeignKey(Review, on_delete= models.CASCADE, related_name='comments')
    date_posted = models.DateTimeField()

class UserProfile(models.Model):
    bio = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    citazione = models.ForeignKey(Citazione, on_delete= models.CASCADE, default=25)
    favorities = models.ManyToManyField(Movie, related_name="favorities", related_query_name="favorities")
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE,default=1)
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)

    def number_of_following(self):
        return self.following.count()


class CinemaClub(models.Model):
    nome = models.CharField(max_length=200)
    bio = models.CharField(max_length=700)
    copertina = models.ForeignKey(Avatar, on_delete= models.CASCADE)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    members = models.ManyToManyField(User,related_name="members", related_query_name="members")
    
    def number_of_members(self):
        return self.members.all().count() + 1

class Post(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=500)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    date_posted = models.DateTimeField()
    group = models.ForeignKey(CinemaClub, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_like')
    
    def number_of_likes(self):
        return self.likes.count()



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


