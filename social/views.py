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