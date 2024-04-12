from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin

from django import forms
from django.contrib import admin

from main.models import Post

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)
