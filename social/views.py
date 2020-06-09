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