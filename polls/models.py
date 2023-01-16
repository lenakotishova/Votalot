from django.db import models
import datetime
from datetime import timedelta
from django.db.models import Sum, Count
from django.contrib.contenttypes.fields import GenericRelation

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


class Question(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date to publish', default=timezone.now)
    created_date = models.DateTimeField('date created', auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_post')

    def __str__(self):
        return self.question_text

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

    def get_absolute_url(self):
        return reverse('polls:details', kwargs={'pk': self.pk})

    @property
    def total_votes(self):
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']

    def total_likes(self):
        return self.likes.count()

    # @property
    # def total_likes(self):
    #     return self.likes.count()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('choice', max_length=40)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.question.question_text, self.question.author)