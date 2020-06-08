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