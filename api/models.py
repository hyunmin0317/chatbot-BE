import jsonfield
from django.db import models


class Answer(models.Model):
    input = models.TextField(unique=True)
    query = jsonfield.JSONField()
    output = jsonfield.JSONField()
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.input


class Result(models.Model):
    uid = models.CharField(max_length=30)
    question = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    pred = models.FloatField()
    result = models.BooleanField(default=True)

    def __str__(self):
        return self.question
