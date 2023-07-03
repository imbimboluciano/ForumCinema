from typing import Any
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from forum.models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'citazione', 'favorities', 'avatar')
    
    favorities = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['descrizione']
        widgets = {
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['descrizione']
        widgets = {
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

class GroupsCreateForm(forms.ModelForm):
    class Meta:
        model = CinemaClub
        fields = ["nome", "bio", "copertina", "members"]
    
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titolo", "descrizione"]
        widgets = {
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
            }