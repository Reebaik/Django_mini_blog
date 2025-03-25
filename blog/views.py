from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q
from .models import BlogPost, BlogAuthor, Comment
from .forms import CommentForm, UserRegistrationForm, BlogPostForm

def index(request):
    """View function for home page of site."""
    blog_posts = BlogPost.objects.all().order_by('-post_date')
    return render(request, 'index.html', {'blog_posts': blog_posts})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    blog_posts = BlogPost.objects.filter(author__user=request.user).order_by('-post_date')
    return render(request, 'blog/profile.html', {'blog_posts': blog_posts})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author, created = BlogAuthor.objects.get_or_create(user=request.user)
            post.author = author
            post.save()
            return redirect('profile')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Create Blog Post'})

class BlogDetailView(generic.DetailView):
    """Generic class-based detail view for a blog."""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    
    def test_func(self):
        post = self.get_object()
        return post.author.user == self.request.user
    
    def get_success_url(self):
        return reverse('profile')

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author.user != request.user:
        messages.error(request, "You can't delete this post!")
        return redirect('profile')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('profile')
    
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})

class BlogListView(generic.ListView):
    """Generic class-based view for a list of blogs."""
    model = BlogPost
    paginate_by = 5

class BloggerListView(generic.ListView):
    """Generic class-based view for a list of bloggers."""
    model = BlogAuthor
    template_name = 'blog/blogger_list.html'

class BloggerDetailView(generic.DetailView):
    """Generic class-based detail view for a blogger."""
    model = BlogAuthor
    template_name = 'blog/blogger_detail.html'

@login_required
def blog_comment_create(request, pk):
    """View function for creating a comment on a blog."""
    blog = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.blog = blog
            comment.save()
            return redirect('blog-detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, 'blog/comment_form.html', context)

@login_required
def comment_edit(request, pk):
    """View function for editing a comment."""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if user is the author of the comment
    if comment.author != request.user:
        messages.error(request, "You can't edit this comment!")
        return redirect('blog-detail', pk=comment.blog.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('blog-detail', pk=comment.blog.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/comment_form.html', {
        'form': form,
        'blog': comment.blog,
        'is_edit': True
    })

@login_required
def comment_delete(request, pk):
    """View function for deleting a comment."""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if user is the author of the comment
    if comment.author != request.user:
        messages.error(request, "You can't delete this comment!")
        return redirect('blog-detail', pk=comment.blog.pk)
    
    blog_pk = comment.blog.pk
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('blog-detail', pk=blog_pk)
    
    return render(request, 'blog/comment_confirm_delete.html', {
        'comment': comment
    })

def search(request):
    """View function for searching blog posts."""
    query = request.GET.get('q', '')
    if query:
        blog_posts = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-post_date')
    else:
        blog_posts = BlogPost.objects.all().order_by('-post_date')
    
    return render(request, 'blog/search_results.html', {
        'blog_posts': blog_posts,
        'query': query
    })
