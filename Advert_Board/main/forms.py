from django import forms
from django.contrib.auth.models import User

from main.models import Post, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']


class ResponseForm(forms.ModelForm):
    text = forms.CharField(
        min_length=10,
        max_length=1000,
        widget=forms.Textarea({'cols': 70, 'rows': 3})
    )

    class Meta:
        model = Response
        fields = ['text']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']