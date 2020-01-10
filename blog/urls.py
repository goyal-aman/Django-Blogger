from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home' ),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='blog-post-detail' ),
    path('post/new/', views.PostCreateView.as_view(), name='blog-post-create' ),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='blog-post-update'),
]
