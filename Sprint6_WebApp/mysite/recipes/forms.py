# recipes/forms.py
from django import forms
from .models import Recipe, Ingredient, Step

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'thumbnail', 'description']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'amount']

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['order', 'text']
