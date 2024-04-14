import random
from string import hexdigits
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail

from Advert_Board.settings import DEFAULT_FROM_EMAIL
from main.models import Post, Response, Verification_Code


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

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = Verification_Code(user_id=user, number=''.join(random.sample(hexdigits, 5)))
        user.save()
        code.save()

        send_mail(
            subject='Код активации',
            message=f'Код для активации аккаунта: {code.number}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user