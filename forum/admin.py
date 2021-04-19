from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ForumUserCreationForm, ForumUserChangeForm
from .models import ForumUser, Thread, Comment, Category

class ForumUserAdmin(UserAdmin):
    add_form = ForumUserCreationForm
    form = ForumUserChangeForm
    model = ForumUser
    list_display = ['email', 'username',]

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'createdBy', 'createdAt']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(ForumUser, ForumUserAdmin)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin);


