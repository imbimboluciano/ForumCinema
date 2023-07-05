from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
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
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }
    
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(GroupsCreateForm, self).__init__(*args, **kwargs)
        print(self.user)
        if self.user is not None:
            actual_user = User.objects.get(pk = self.user)
            
            possible_members = []
            for user in User.objects.all():
                if user.userprofile in actual_user.userprofile.followers.all() and user.userprofile in actual_user.userprofile.following.all():
                    possible_members.append(user.pk)
            self.fields['members'].queryset = User.objects.all().filter(pk__in=possible_members).exclude(pk=actual_user.pk).exclude(is_staff=True)
        
        

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titolo", "descrizione"]
        widgets = {
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
            }
        
class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'descrizione']
        widgets = {
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
            }