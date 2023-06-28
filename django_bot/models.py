from django.db import models


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question


class Keyword(models.Model):
    keyword = models.TextField()

    def __str__(self):
        return self.keyword


class QuestionKeyword(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)


class AllowedLinks(models.Model):
    link = models.TextField()

    def __str__(self):
        return self.link
