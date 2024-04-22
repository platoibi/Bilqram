from django.urls import path

from . import views

app_name = 'Bilqram'

urlpatterns = [
    path('', views.index, name='home'),
    path('users', views.users, name='users'),
    path('user/<str:username>', views.user, name='user'),
    path('newBlog', views.createBlogPage, name='newBlog'),
    path('newBlogAction', views.createBlogAction, name='newBlogAction'),
    path('blog/<int:blog_id>', views.blog, name='blog'),
    path('blogs', views.blogs, name='blogs'),
    path('register', views.register, name='register'),
    path('user_created', views.user_created, name='user_created'),
    path('login/', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout')
]