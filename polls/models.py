from django.db import models
import datetime

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


class Question(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
    )
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date to publish')
    created_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

    def get_absolute_url(self):
        return reverse('polls:details', kwargs={'pk': self.pk})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
