from django.contrib import admin

# Register your models here.
from .models import User, Content, Blog, Comment, Like
admin.site.register(User)
admin.site.register(Content)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)