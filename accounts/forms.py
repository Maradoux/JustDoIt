from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False
    )
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'profile_picture', 
            'bio', 
            'role', 
            'department'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile = user.profile
            profile.profile_picture = self.cleaned_data.get('profile_picture')
            profile.bio = self.cleaned_data.get('bio')
            profile.role = self.cleaned_data.get('role')
            profile.department = self.cleaned_data.get('department')
            profile.save()
        
        return user