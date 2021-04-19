from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
import uuid


class ForumUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    createdBy = models.ForeignKey('ForumUser', related_name='categories', default='', on_delete=models.CASCADE)

    def __str__(self):
        selfString = self.name + " by " + self.createdBy.username
        return selfString


class Thread(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    createdBy = models.ForeignKey('ForumUser', related_name='userthreads', default='', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    body = RichTextField()
    category = models.ForeignKey('Category', related_name='categorythreads', on_delete=models.CASCADE)
    thread_identifier = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    tags = TaggableManager()

    def __str__(self):
        selfString = self.title + " by " + self.createdBy.username
        return selfString 

class Comment(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    createdBy = models.ForeignKey('ForumUser', related_name='comments', default='', on_delete=models.CASCADE)
    content = RichTextField()
    forumThread = models.ForeignKey('Thread', to_field='thread_identifier', related_name='threadcomments', blank=True, null=True, on_delete=models.CASCADE)
    comment_identifier = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    def __str__(self):
        selfString = "Comment by " + self.createdBy.username
        return selfString