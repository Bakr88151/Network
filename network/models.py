from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField('User', related_name='followers')


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name='posts')
    post = models.TextField(blank=False, max_length=2064)
    likes = models.IntegerField(default=0, auto_created=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField("User", blank=True, related_name='liked')

    def serialize(self, user):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "poster_id": self.poster.id,
            "content": self.post,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            'liked': user in self.liked.all()
        }


