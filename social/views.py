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