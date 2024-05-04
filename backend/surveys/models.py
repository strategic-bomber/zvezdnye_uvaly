from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Survey(models.Model):
    """Survey application"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    map = models.ImageField()
    coordinates = models.JSONField(default=list, blank=True)  # list of coords
    total_budget = models.IntegerField()

    def __str__(self):
        return f"Опрос '{self.name}'"

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class SurveyChoice(models.Model):
    """Application choices"""
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return f"Объект '{self.name}' в опросе '{self.survey.name}'"

    class Meta:
        verbose_name = "Объект опроса"
        verbose_name_plural = "Объекты опроса"


class ImageModel(models.Model):
    """Image model"""
    image = models.ImageField()
    choice = models.ForeignKey(SurveyChoice, on_delete=models.CASCADE, related_name="images")


class UserChoice(models.Model):
    choice = models.ForeignKey(SurveyChoice,
                               on_delete=models.CASCADE)

    coordinates = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    session_key = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
