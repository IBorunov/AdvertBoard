from django import forms

from main.models import Post, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['post', 'text']
