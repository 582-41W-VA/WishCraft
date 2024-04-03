"""
This file contains the models for the app.

Models:
- Card: Model for storing card details.
- Tag: Model for storing tag details.
- Comment: Model for storing comment details.
- Like: Model for storing like details.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Card(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag")
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


DEFAULT_TAGS = [
    ("fashion", "Fashion"),
    ("home decor", "Home Decor"),
    ("food & recipe", "Food & Recipe"),
    ("travel", "Travel"),
    ("art & design", "Art & Design"),
    ("photography", "Photography"),
    ("diy & craft", "DIY & Craft"),
    ("health & fitness", "Health & Fitness"),
    ("tech", "Tech"),
    ("books & literature", "Books & Literature"),
]


class Tag(models.Model):
    name = models.CharField(max_length=255, choices=DEFAULT_TAGS)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.card.title}"
