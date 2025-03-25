from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('bloggers/', views.BloggerListView.as_view(), name='blogger-list'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('new/', views.blog_create, name='blog-create'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', views.blog_delete, name='blog-delete'),
    path('<int:pk>/comment/', views.blog_comment_create, name='blog-comment-create'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment-edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),
    path('search/', views.search, name='search'),
] 