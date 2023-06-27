from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from forum.models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'citazione', 'favorities')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['descrizione']