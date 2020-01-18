from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Profile
# Create your views here.


class UserProfileListView(ListView):
    '''
    urlconf name: 'blog-post-user'
    url-parameter: username

    modified get_queryset, return only required user post object
    '''
    model = Post
    template_name = 'blog/post_user.html'
    context_object_name = 'object'
    ordering = ['-date_update']
    paginate_by = 10

    def is_following(self, **kwargs):
        return self.request.user.profile.isfollowing.filter(user__username=self.kwargs.get('username')).count() == 1

    def get_queryset(self):
        self.profile_user = get_object_or_404(
            get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.profile_user).order_by('-date_update')

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileListView, self).get_context_data(**kwargs)
        context['user_object'] = get_user_model().objects.get(
            username=self.kwargs.get('username'))
        return context


class PostListView(LoginRequiredMixin, ListView):
    '''
    urlconf name: 'blog-home'


    updated get_queryset to contain logged in user post
    '''
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>/.html
    context_object_name = 'posts'
    ordering = ['-date_update']
    paginate_by = 10

    def get_queryset(self):
        user_post = Post.objects.filter(author=self.request.user)
        # .order_by('-date_update')
        qs = Post.objects.filter(
            author__profile__followers=self.request.user.profile)
        return qs.union(user_post).order_by('-date_update')


class PostDetailView(DetailView):
    '''
    urlconf name: 'blog-post-detail'
    url-parameter: post.pk
    template : 'post_detail.html'
    '''
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    '''
    urlconf : 'blog-post-create'
    template used : post_form.html
    '''
    model = Post
    fields = ['title', 'content']  # <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    urlconf : 'blog-post-update'
    url parameter : post.pk

    template used : post_form.html
    '''

    model = Post
    fields = ['title', 'content']  # <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.date_updated = timezone.now()
        form.instance.is_postupdated = True
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    urlconf : 'blog-post-delete'
    url parameter : post.pk

    template used : 'post_confirm_delete.html'
    '''
    
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True


def show_followers(request, **kwargs):
    '''
    url conf name : 'user-follower'
    url parameter: 'username'
    '''
    user = get_user_model().objects.get(username=kwargs.get('username'))
    context = {

        'followers': user.profile.followedby.all().order_by('user__username')
    }
    return render(request, 'blog/followers.html', context)


def show_following(request, **kwargs):
    user = get_user_model().objects.get(username=kwargs.get('username'))
    context = {

        'followings': user.profile.isfollowing.all()
    }
    return render(request, 'blog/following.html', context)
