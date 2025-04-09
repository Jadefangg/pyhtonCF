#recipes/forms.py
from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'category']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4}),
        }