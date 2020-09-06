from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import  ModelFormMixin
from .models import Post, Tag, Comment, Reply
from .widgets import CustomCheckboxSelectMultiple
from .forms import TagCreateForm, CommentCreateForm, ReplyCreateForm

'''------------------------------------記事関連------------------------------------
'''

'''ホーム'''
class PostListView(ListView):
    model = Post
    template_name = "original_blog/home.html"
    ordering = ["-date_posted"]
    paginate_by = 10

'''ユーザ別の記事一覧'''
class UserPostListView(ListView):
    model = Post
    template_name = "original_blog/user_posts.html"
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by("-date_posted")

'''タグ別の記事一覧'''
class TagPostListView(ListView):
    model = Post
    template_name = "original_blog/tag_posts.html"
    paginate_by = 10

    def get_queryset(self):
        designated_tag = get_object_or_404(Tag, name=self.kwargs.get('tagname'))
        return Post.objects.filter(tags=designated_tag).order_by("-date_posted")

'''記事の詳細'''
class PostDetailView(DetailView):
    model = Post

'''記事の投稿'''
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['is_public', 'title', 'content', 'tags']
        widgets = {
            'tags' : CustomCheckboxSelectMultiple
        }

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

'''記事の更新'''
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

'''記事の削除'''
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


'''------------------------------------タグ関連------------------------------------
'''
class TagManageView(ListView, ModelFormMixin):
    model = Tag
    template_name = "original_blog/manage_tag.html"
    form_class = TagCreateForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.object = self.form.save()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TagManageView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        return context


'''------------------------------------コメント関連------------------------------------
'''
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk = post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.save()
        return redirect('post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyCreateForm
    template_name = "original_blog/comment_form.html"

    def form_valid(self, form):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()
        return redirect('post_detail', pk=comment.target.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context['post'] = comment.target
        return context

'''------------------------------------その他------------------------------------
'''
def about(request):
    return render(request, 'original_blog/about.html', {'title':'About'})
