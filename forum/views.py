from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import ForumUser, Thread, Comment, Category
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .serializers import ForumUserSerializer, GroupSerializer, ThreadSerializer, CommentSerializer, CategorySerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class ForumUserViewSet(viewsets.ModelViewSet):
    """ endpoint for view or edit """
    queryset = ForumUser.objects.all().order_by('-date_joined')
    serializer_class = ForumUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

class GroupViewSet(viewsets.ModelViewSet):
    """ endpoint for view or edit """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all().order_by('-createdAt')
    serializer_class = ThreadSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'thread_identifier']

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('createdAt')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)

    def get_queryset(self):
        my_param = self.request.GET.get('forumThread')
        if my_param is None:
            return self.queryset
        else:
            forumThreadId = self.request.query_params['forumThread']
            if forumThreadId:
                print('forumThread is not empty')
                self.queryset = Comment.objects.filter(forumThread=forumThreadId)
                return self.queryset
            else:
                print('forum thread is empty')
                return self.queryset

class CreateUserView(CreateAPIView):
    model = UserModel
    permission_classes = [permissions.AllowAny]
    serializer_class = ForumUserSerializer

    
    @classmethod
    def get_extra_actions(cls):
        return []