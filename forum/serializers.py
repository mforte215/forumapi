from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import ForumUser, Thread, Comment, Category
from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class ShortHandCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

class ShortHandForumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumUser
        fields = ['username']

class ForumUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='createdBy.username', read_only=True)
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'forumThread', 'comment_identifier', 'createdBy', 'username', 'createdAt', 'is_owner']
    
    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.createdBy.id


class ShorHandThreadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='createdBy.username', read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'title', 'createdBy', 'thread_identifier', 'createdAt', 'username', 'is_owner']
    
    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.createdBy.id


class ThreadSerializer(TaggitSerializer, serializers.ModelSerializer):
    threadcomments = CommentSerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    is_owner = serializers.SerializerMethodField()
    categoryName = serializers.CharField(source='category.name', read_only=True)
    username = serializers.CharField(source='createdBy.username', read_only=True)


    class Meta:
        model = Thread
        fields = ['id', 'title', 'category', 'categoryName', 'thread_identifier', 'body', 'createdBy', 'username', 'createdAt', 'threadcomments', 'tags', 'is_owner']
    
    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.createdBy.id

class CategorySerializer(serializers.ModelSerializer):
    categorythreads = ShorHandThreadSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'categorythreads']


    

