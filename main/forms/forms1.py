from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from main.models import Group,Course
from main.models.auth import User





class AdminCreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'ut', 'specialty', 'level', 'username', 'email', 'password']

    def save(self):
        user = super().save()              # обычный save()
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class AdminCreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'mentor']




class AdminCreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'course', 'duration', 'status', 'start_date']