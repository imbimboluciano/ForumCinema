from django import template
from polls.models import *

register = template.Library()

@register.simple_tag
def user_can_vote(user, poll):
    if poll.user_can_vote(user):
        return False
    
    return True

@register.simple_tag
def user_vote(user, poll):
    return poll.uservote(user)