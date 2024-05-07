from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from Bilqram.models import User, Blog, Comment, Like
from .forms import LoginForm
from django.contrib.auth.models import User as U


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
    u = get_object_or_404(User, username=username)
    context = {
        'User': u
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
        'blog': b,
        'comments': Comment.objects.filter(par_blog=b),
        'likes': len(Like.objects.filter(blog=b)),
        'liked': len(Like.objects.filter(user=get_object_or_404(User, username=request.user.username), blog=b)) == 1 if request.user.is_authenticated else False
    }
    print(context['liked'])
    return render(request, 'Bilqram/blog.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.password = password
            user.save()
            mainUser = U.objects.create_user(username=username, password=password)
            mainUser.save()
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
            # u = get_object_or_404(User, username=username)
            # print(u.password)
            user = authenticate(request, username=username, password=password)
            print(user)
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


def newComment(request, blog_id):
    if request.method == 'POST':
        b = get_object_or_404(Blog, pk=blog_id)
        c = Comment(par_blog=b, content=request.POST['comment'],
                    author=get_object_or_404(User, username=request.user.username), editable=True,
                    pub_date=timezone.now())
        c.save()
        return redirect('Bilqram:blog', blog_id=blog_id)
    else:
        return redirect('Bilqram:home')


def like(request, blog_id):
    if not request.user.is_authenticated:
        return redirect('Bilqram:login')
    b = get_object_or_404(Blog, pk=blog_id)
    curLike = Like.objects.filter(user=get_object_or_404(User, username=request.user.username), blog=b)
    if len(curLike) == 0:
        l = Like(blog=b, user=get_object_or_404(User, username=request.user.username), date=timezone.now())
        l.save()
    else:
        curLike.delete()
    return redirect('Bilqram:blog', blog_id=blog_id)
