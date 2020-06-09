from django.urls import path,re_path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('posts/', views.post, name='posts'),
    path('create_post/', views.create_post, name='createpost'),
    path('comment/<post_id>', views.comment, name='comment'),
    path('add_comment/<poat_id>', views.add_comment, name='add_comment')
]