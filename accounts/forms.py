from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Service, Review, Demand

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('artisan', 'Artisan'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    address = forms.CharField(max_length=255)  # Ajout du champ address

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'user_type', 'address']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['type', 'address', 'phone_number', 'image']

class UserProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(max_length=255)  # Ajout du champ address

    class Meta:
        model = UserProfile
        fields = ['type', 'address', 'phone_number', 'image']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'demand', 'contact_number', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }

class DemandForm(forms.ModelForm):
    requested_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Demand
        fields = ['requested_date', 'start_time', 'end_time']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
