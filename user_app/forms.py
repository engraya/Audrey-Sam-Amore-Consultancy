from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class AdminRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your First Name'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Last Name'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Email'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})


    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']



class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Password'})
        
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'

class ClientLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Password'})
        
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'




class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['age'].widget.attrs.update({'class' : 'form-control'})
        self.fields['seeking'].widget.attrs.update({'class' : 'form-control'})
        self.fields['about'].widget.attrs.update({'class' : 'form-control'})
        self.fields['state'].widget.attrs.update({'class' : 'form-control'})
        self.fields['city'].widget.attrs.update({'class' : 'form-control'})
        self.fields['dateOfBirth'].widget.attrs.update({'class' : 'form-control'})
        self.fields['relationshipStatus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['kidsStatus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['hobbyList'].widget.attrs.update({'class' : 'form-control'})
        self.fields['partnerPreference'].widget.attrs.update({'class' : 'form-control'})
        self.fields['complexion'].widget.attrs.update({'class' : 'form-control'})
        self.fields['seekingRelationship'].widget.attrs.update({'class' : 'form-control'})
        self.fields['country'].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'age', 'gender', 'seeking', 'about', 'state', 'city', 'dateOfBirth', 'relationshipStatus', 'kidsStatus', 'hobbyList', 'partnerPreference', 'complexion', 'seekingRelationship', 'country']

class SignUpStepOneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age']

class SignUpStepTwoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['state','city', 'gender', 'seeking']

class SignUpStepThreeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'about']



