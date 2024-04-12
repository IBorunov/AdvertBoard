from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Advert_Board.settings import DEFAULT_FROM_EMAIL
from main.models import Post, Response


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()



class PostCreate(CreateView):
    permission_required = ('main.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        # raise Exception(f'{self.request.user} {self.request.user.is_authenticated}')
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs


@method_decorator(login_required, name='dispatch')
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs


@method_decorator(login_required, name='dispatch')
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        resp = form.save(commit=False)
        resp.save()
        send_mail(
            subject=f'На Ваш пост {resp.post.title} откликнулся {resp.user.username}.',
            message=resp.text,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[resp.post.author.email]
        )

        return super().form_valid(form)


class ResponseDetail(DetailView):
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'
    queryset = Response.objects.all()


@method_decorator(login_required, name='dispatch')
class ComUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_response',)
    form_class = ResponseForm
    model = Response
    template_name = 'com_edit.html'

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs


@method_decorator(login_required, name='dispatch')
class ComDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_response',)
    model = Response
    template_name = 'resp_delete.html'
    success_url = reverse_lazy('posts_list')


class ComsSearch(ListView):
    model = Response
    ordering = '-time_in'
    template_name = 'resp_search.html'
    context_object_name = 'resp_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = Response.objects.filter(post__author_id=self.request.user.pk)
        self.filterset = Response_Filter(self.request.GET, queryset, request=self.request.user.pk)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context