from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from Bilqram.models import User, Blog
from .forms import LoginForm


# Create your views here.
def index(request):
    return render(request, 'Bilqram/home.html')


def users(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'Bilqram/users.html', context)


def user(request, username: str):
    u = get_object_or_404(User, username=username.lower())
    context = {
        'user': u
    }
    return render(request, 'Bilqram/user.html', context)


def createBlogPage(request):
    if request.user.is_authenticated:
        return render(request, 'Bilqram/createBlog.html')
    else:
        return redirect('Bilqram:login')


def createBlogAction(request):
    d = request.POST
    print(d)
    b = Blog(title=d['title'], content=d['content'],
             author=get_object_or_404(User, id=request.user.id), pub_date=timezone.now(), editable=True)
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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            messages.success(request, f'Account created for {username} {password}!')
            return redirect('Bilqram:user_created')
    else:
        form = UserRegistrationForm()
    return render(request, 'Bilqram/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password']
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or homepage
                return redirect('Bilqram:blogs')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'Bilqram/login.html', {'form': form})


def user_created(request):
    return render(request, 'Bilqram/user_created.html')


def user_logout(request):
    logout(request)
    return redirect('Bilqram:home')
