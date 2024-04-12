from django import forms
from django.contrib.auth.models import User

from main.models import Post, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['post', 'text']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']