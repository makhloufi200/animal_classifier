from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import animal

class AnimalsForm(forms.ModelForm):
    class Meta:
        model = animal
        fields = ['image']
