from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email', 
            'password1', 
            'password2', 
        ]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'department']