import datetime

#VOTERS
from django.contrib.auth.models import User

#MISC
from django.utils import timezone
from django.db import models
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name="voted_choices", blank=True)

    def __str__(self):
        return self.choice_text
    
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    party = models.CharField(max_length=100)
    biography = models.TextField()
    photo = models.ImageField(upload_to='candidates/')
    
    def __str__(self):
        return self.name