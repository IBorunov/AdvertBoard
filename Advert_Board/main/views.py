from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Advert_Board.settings import DEFAULT_FROM_EMAIL
from main.filters import ResponseFilter
from main.forms import PostForm, ResponseForm, ProfileForm, CommonSignupForm
from main.models import Post, Response, Verification_Code


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

class MyPostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'my_posts.html'
    context_object_name = 'my_posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(author_id=self.request.user.pk)
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.pk)
        return self.filterset.qs

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
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'my_responses.html'
    context_object_name = 'my_responses'
    paginate_by = 10

    def get_queryset(self):
        """Get all the responds to user's adverts"""
        queryset = Response.objects.filter(post_id__author_id=self.request.user).order_by('-time_in')
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'respond.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs):
        """Get correct post from url-path"""
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        resp = form.save(commit=False)
        resp.user = self.request.user
        resp.post = Post.objects.get(id=self.kwargs['pk'])
        resp.save()


        send_mail(
            subject=f'На Ваш пост {resp.post.title} откликнулся {resp.user.username}.',
            message=resp.text,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[resp.post.author.email]
        )

        return super().form_valid(form)


@login_required
def accept_response(request, pk):
    response = Response.objects.get(id=pk)
    response.is_accepted = True
    response.save()
    return redirect('my_responses')

@login_required
def delete_response(request, pk):
    Response.objects.get(id=pk).delete()
    return redirect('my_responses')

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'account/profile_edit.html'
    success_url = '/'


class CategoryView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        object = get_object_or_404(Post, category=self.kwargs['category'])
        self.category = object.category
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ConfirmUser(UpdateView):
    model = Verification_Code
    form_class = CommonSignupForm
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code_obj = Verification_Code.objects.filter(number=request.POST['code'])
            if code_obj.exists():
                user = User.objects.get(id=code_obj[0].user_id.id)
                user.is_active = True
                user.save()
                code_obj[0].number = None
                code_obj[0].save()
                return redirect('/')
            else:
                return render(self.request, template_name='invalid_code.html')
        return redirect('/')