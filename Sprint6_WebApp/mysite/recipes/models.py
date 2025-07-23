from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title       = models.CharField(max_length=200)
    thumbnail   = models.ImageField(upload_to='thumbnails/')
    description = models.TextField(blank=True)
    # star rating average (0–5)
    rating_avg  = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name   = models.CharField(max_length=200)
    amount = models.CharField(max_length=100)

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    order  = models.PositiveSmallIntegerField()
    text   = models.TextField()

    class Meta:
        ordering = ['order']

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    score  = models.PositiveSmallIntegerField()  # 1 to 5
