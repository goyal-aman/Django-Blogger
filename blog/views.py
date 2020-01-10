from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>/.html
    context_object_name = 'posts'
    ordering = ['-date_update']

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
