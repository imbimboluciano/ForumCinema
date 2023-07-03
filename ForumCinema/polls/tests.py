from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Poll, Vote, CinemaClub
from forum.models import Avatar, Citazione, UserProfile


class PollModelTest(TestCase):
    def test_user_can_vote(self):
        user = User.objects.create_user(username='john', password='rambo')
        citazione = Citazione.objects.create(pk = 25,descrizione="djiejdiej")
        avatar = Avatar.objects.create(pk = 1, image="hhdfhedf")
        userprofile = UserProfile.objects.get(user = user)
        userprofile.citazione = citazione
        userprofile.avatar = avatar
        
        
        group = CinemaClub.objects.create(creator=user, copertina = avatar)
        poll = Poll.objects.create(owner=user, group =group)
       
        self.assertTrue(poll.user_can_vote(user))

        choice = poll.choice_set.create(choice_text='pizza')
        Vote.objects.create(user=user, poll=poll, choice=choice)
        self.assertFalse(poll.user_can_vote(user))