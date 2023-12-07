
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:page_number>", views.posts, name='posts'),
    path('submitpost', views.submit_post),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('following', views.followig, name='followimg'),
    path('postsfollowing/<int:page_number>', views.postsfollowing),
    path('like', views.like, name='like'),
    path('profileposts/<int:page_number>', views.profileposts)
]
