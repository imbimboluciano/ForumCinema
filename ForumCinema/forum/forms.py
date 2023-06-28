from typing import Any
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from forum.models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'citazione', 'favorities', 'avatar')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['descrizione']

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['descrizione']