from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone

from Bilqram.models import User, Blog


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the bilqram index.")


def users(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'Bilqram/users.html', context)


def user(request, username):
    u = get_object_or_404(User, username=username)
    context = {
        'user': u
    }
    return render(request, 'Bilqram/user.html', context)


def createBlogPage(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'Bilqram/createBlog.html', context)


def createBlogAction(request):
    d = request.POST
    print(d)
    b = Blog(title=d['title'], content=d['content'],
             author=get_object_or_404(User, id=int(d['author'])), pub_date=timezone.now(), editable=True)
    b.save()
    return redirect('Bilqram:blogs')


def blogs(request):
    blog_list = Blog.objects.all()
    context = {
        'blogs': blog_list
    }
    return render(request, 'Bilqram/blogs.html', context)


def blog(request, blog_id):
    b = get_object_or_404(Blog, id=blog_id)
    context = {
        'blog': b
    }
    return render(request, 'Bilqram/blog.html', context)