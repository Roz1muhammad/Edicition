from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Ball

class BallForm(forms.ModelForm):
    ball = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={'max': 5, 'min': 0})
    )

    class Meta:
        model = Ball
        fields = '__all__'
