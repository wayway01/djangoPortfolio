from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, PostCreateForm, TagManageView, TagPostListView, CommentCreateView, ReplyCreateView
from . import views as posts_views

urlpatterns = [
    path('', PostListView.as_view(), name="blog_home"),
    path('about/', posts_views.about, name="blog_about"),
    path('post/new', PostCreateView.as_view() , name="post_create"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post_update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name="comment_create"),
    path('post/<int:pk>/reply/', ReplyCreateView.as_view(), name="reply_create"),
    path('tags', TagManageView.as_view(), name="tag_manage"),
    path('tag/<str:tagname>', TagPostListView.as_view(), name="tag_post"),
    path('user/<str:username>', UserPostListView.as_view(), name="user_post"),
]