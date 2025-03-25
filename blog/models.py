from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class BlogAuthor(models.Model):
    """Model representing a blog author."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, help_text="Enter your bio details here.")

    class Meta:
        ordering = ['user__username']

    def get_absolute_url(self):
        """Returns the url to access a particular blog-author instance."""
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

class BlogPost(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, help_text="Enter your blog text here.")
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        """Returns the url to access a particular blog instance."""
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

class Comment(models.Model):
    """Model representing a comment on a blog post."""
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        """String for representing the Model object."""
        len_title = 75
        if len(self.description) > len_title:
            return self.description[:len_title] + '...'
        return self.description
