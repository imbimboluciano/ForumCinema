from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from forum.models import *



class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email',max_length=200)
    first_name = forms.CharField(required=True, label="Nome", max_length=200)
    last_name = forms.CharField(required=True, label="Cognome", max_length=200)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
    

