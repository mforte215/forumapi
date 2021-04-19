from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ForumUser

class ForumUserCreationForm(UserCreationForm):
    
    class Meta:
        model = ForumUser
        fields = ('username', 'email')

class ForumUserChangeForm(UserChangeForm):

    class Meta:
        model = ForumUser
        fields = ('username', 'email')
