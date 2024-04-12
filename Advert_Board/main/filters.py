import django_filters
from django import forms
from .models import Response, Post
from urllib import request


class ResponseFilter(django_filters.FilterSet):
    class Meta:
        model = Response
        fields = ('post',)

