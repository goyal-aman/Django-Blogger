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
    modified get_queryset, return only required user object
    kwarg: username
    '''
    model = Post
    template_name = 'blog/profile_list.html'
    context_object_name = 'object'
    paginate_by = 10
    

    # def get_user(self, **kwargs):
        # '''return user object with username = self.kwargs.get('username')'''
        # return get_user_model().objects.get(username=self.kwargs.get('username'))

    def is_following(self, **kwargs):
        return self.request.user.profile.isfollowing.filter(user__username=self.kwargs.get('username')).count() == 1
    
    def get_queryset(self):
        self.profile_user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.profile_user)
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileListView, self).get_context_data(**kwargs)
        context['user_object'] = get_user_model().objects.get(username=self.kwargs.get('username'))
        # context['if_following'] = self.request.user.profile.isfollowing.filter(user__username=self.kwargs.get('username')).count() == 1
        print('this is context', context)
        return context


class PostListView(LoginRequiredMixin  ,ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>/.html
    context_object_name = 'posts'
    ordering = ['-date_update']
    paginate_by = 10 

    def get_queryset(self):
        user_post = Post.objects.filter(author=self.request.user)
        qs = Post.objects.filter(author__profile__followers=self.request.user.profile)  #.order_by('-date_update')
        return qs.union(user_post).order_by('-date_update')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields = ['title', 'content'] # <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] # <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.date_updated = timezone.now()
        form.instance.is_postupdated = True
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

class PostDeleteView( LoginRequiredMixin, UserPassesTestMixin , DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
    
def show_followers(request, **kwargs):
    context = {

        'followers' : request.user.profile.followedby.all()
    }
    return render(request, 'blog/followers.html', context)


def show_following(request, **kwargs):
    context = {

        'followings' : request.user.profile.isfollowing.all()
    }
    return render(request, 'blog/following.html', context)

