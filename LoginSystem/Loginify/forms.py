from django import forms
from .models import UserDetails


class SignupForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password']
    
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, required=True)         
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")