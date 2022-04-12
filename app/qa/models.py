from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.urls import reverse


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')

    def zero_answers(self):
        return self.annotate(
            num_answers=Count('answers')).filter(num_answers=0)


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='question_author', null=True)
    likes = models.ManyToManyField(User, related_name='liked_by_user')
    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('qa:single_question_url',
                       kwargs={'question_id': self.pk})

    def get_update_url(self):
        return reverse('qa:question_update_url',
                       kwargs={'question_id': self.pk})

    def get_delete_url(self):
        return reverse('qa:question_delete_url',
                       kwargs={'question_id': self.pk})

    def get_like_url(self):
        return reverse('qa:question_like_url', kwargs={'question_id': self.pk})

    def get_total_rating(self):
        return self.rating + self.likes.count()

    def __str__(self):
        return self.title


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('qa:single_answer_url', kwargs={'answer_id': self.pk})

    def get_update_url(self):
        return reverse('qa:answer_update_url', kwargs={'answer_id': self.pk})

    def get_delete_url(self):
        return reverse('qa:answer_delete_url', kwargs={'answer_id': self.pk})

    def __str__(self):
        return f'Answer {self.pk} for question {self.question}'
