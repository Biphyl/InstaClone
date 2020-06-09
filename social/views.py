from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from .models import Profile,Post,User,Comment,Following
from django.contrib import messages
from .forms import UserCreationForm,UserUpdateForm,CommentForm,ProfileUpdateForm,PostForm
from django.contrib.auth.decorators import login_required



def post(request):
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    comments = Comment.objects.all()
    comment_form = CommentForm()

    context = {
        "posts":posts,
        "comments":comments,
        "users":users,
        "comment_form":comment_form
    }

    return render(request, 'posts.html', context)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'You post have been created successfully!!')
            return redirect('posts')
    else:
        form = PostForm()
    context = {
        "form":form,
    }
    return render(request, 'create_post.html', context)

def comment(request, post_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = Post.get_post(post_id)
            comment.post = post
            comment.save()
            return redirect('posts')
        else:
            comment_form = CommentForm()
        context = {
            "comment_form":comment_form,
        }
        return render(request, 'posts.html', context)

def add_comment(request, post_id):
    posts = Post.objects.get(pk=post_id)
    context={
        "posts":posts,
    }
    return render(request, 'comments.html', context)


def profile(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successfully updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'user_form':user_form,
    'profile_form':profile_form,
    'posts':posts,
    }
    return render(request, 'profile.html', context)

def search_user(request):
    if 'post' in request.GET and request.GET['post']:
        search_term = request.GET["post"]
        searched_posts = Post.search_by_author(search_term)
        message = f'search_term'
        author = User.objects.all()
        context = {
            "author":author,
            "posts":searched_posts,
            "message":message,

        }
        return render(request, 'search.html', context)
    else:
        message = "You haven't searched for any user"
        context = {
            "message":message,
        }
        return render(request, 'search.html', context)


def follow(request,operation,pk):
    new_follower = User.objects.get(pk=pk)
    if operation == 'add':
        Following.make_user(request.user, new_follower)
    elif operation == 'remove':
        Following.loose_user(request.user, new_follower)

    return redirect('posts')

def likes(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked=True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password1=form.cleaned_data['password1']
            recipient=User(username=username,email=email)
            try:
                send_welcome_email(username,email)
                messages.success(request, f'Account has been created successfully!')
            except:
                print('error')
            return redirect('login')

    else:
        form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'users/register.html', context)