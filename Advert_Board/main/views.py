from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Advert_Board.settings import DEFAULT_FROM_EMAIL
from main.filters import ResponseFilter
from main.forms import PostForm, ResponseForm, ProfileForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user.is_authenticated
        return context



class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('main.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class ResponseCreate(CreateView):
    permission_required = ('announcement.add_comment',)
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'

    def form_valid(self, form):
        resp = form.save(commit=False)
        resp.user = self.request.user.user
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


class ResponseUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_response',)
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_response',)
    model = Response
    template_name = 'resp_delete.html'
    success_url = reverse_lazy('posts_list')


class ResponseList(ListView):
    model = Response
    ordering = '-time_in'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Response.objects.filter(post__author_id=self.request.user.pk)
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.pk)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

@login_required
def accept_response(request, pk):
    response = Response.objects.get(id=pk)
    response.is_accepted = True
    response.save()
    return redirect('response_list')

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'account/profile_edit.html'
    success_url = '/'