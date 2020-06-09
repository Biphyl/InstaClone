from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.http import Http404
from django.dispatch import receiver



class Post(models.Model):
    author = models.ForeignKey('auth.user',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    caption = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return f'{self.author} Post'

    class Meta:
        db_table = 'post'
        ordering = ['-created_date']

    def addlikes(self):
        self.likes.count()

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def search_by_author(cls,search_term):
        image = cls.objects.filter(author__username__icontains=search_term)
        return image

    @classmethod
    def get_post(cls,id):
        try:
            post = Post.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404()
        return post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics/')
    bio = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        db_table = 'profile'

    @receiver(post_save, sender=User)
    def update_create_profile(sender,instance,created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


    def save_profile(self):
        self.save()
        
    def delete_profile(self):
        self.delete()
    
    @classmethod   
    def update_bio(cls,id,new_bio):
        cls.objects.filter(pk = id).update(bio=new_bio)
        new_bio_object = cls.objects.get(bio = new_bio)
        new_bio = new_bio_object.bio
        return new_bio

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.post.author}, {self.user.username}'

    class Meta:
        db_table = 'comment'

    def save_comment(self):
        self.save()


class Following(models.Model):
    users = models.ManyToManyField(User, related_name='friend_set')
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.PROTECT, null=True)
    
    @classmethod
    def make_user(cls,current_user,new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def loose_user(cls,current_user,new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)