from django import template
from polls.models import *
from forum.models import *
from django.shortcuts import get_object_or_404

register = template.Library()

@register.simple_tag
def user_can_vote(user, poll):
    if poll.user_can_vote(user):
        return False
    
    return True

@register.simple_tag
def user_vote(user, poll):
    return poll.uservote(user)

@register.simple_tag
def post_like(user, post):
    likes_connected = get_object_or_404(Post, id=post)
    liked = False
    if likes_connected.likes.filter(id=user).exists():
        liked = True
    return liked