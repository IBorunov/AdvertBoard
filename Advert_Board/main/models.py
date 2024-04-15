from datetime import datetime

from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

tanks = 'Танки'
hils = 'Хилы'
dd = 'ДД'
merchants = 'Торговцы'
guild_masters = 'Гилдмастеры'
quest_givers = 'Квестгиверы'
blacksmiths = 'Кузнецы'
tanners = 'Кожевники'
potion_makers = 'Зельевары'
spell_masters = 'Мастера заклинаний'

CATEGORY = [
    (tanks, 'Танки'),
    (hils, 'Хилы'),
    (dd, 'ДД'),
    (merchants, 'Торговцы'),
    (guild_masters, 'Гилдмастеры'),
    (quest_givers, 'Квестгиверы'),
    (blacksmiths, 'Кузнецы'),
    (tanners, 'Кожевники'),
    (potion_makers, 'Зельевары'),
    (spell_masters, 'Мастера заклинаний'),
]


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY)
    title = models.CharField(max_length=250, unique=True)
    content = RichTextField()


    def __str__(self):
        username = self.author.username
        return f'{self.title} by {username}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        username = self.user.username
        return f'{self.text} from {username}'


class Verification_Code(models.Model):
    number = models.CharField(max_length=15, blank=True, null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

class Notification(models.Model):
    """Модель для отправки пользователям уведомлений через админку"""
    title = models.CharField(max_length=220)
    text = models.TextField()

    def __str__(self):
        return self.title

