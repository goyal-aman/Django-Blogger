from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home' ),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='blog-post-detail' ),
    path('post/new/', views.PostCreateView.as_view(), name='blog-post-create' ),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='blog-post-update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='blog-post-delete'),
    path('post/<str:username>', views.UserPostListView.as_view(), name='blog-post-user'),
]
