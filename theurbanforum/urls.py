from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from forum import views

router = routers.DefaultRouter()
router.register(r'forumusers', views.ForumUserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'threads', views.ThreadViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.CreateUserView.as_view())
]


