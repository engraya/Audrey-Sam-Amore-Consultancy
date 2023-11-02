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



class ClientRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your First Name'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Last Name'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})


    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


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
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs.update({'class' : 'form-control'})
        self.fields['seeking'].widget.attrs.update({'class' : 'form-control'})
        self.fields['about'].widget.attrs.update({'class' : 'form-control'})
        self.fields['state'].widget.attrs.update({'class' : 'form-control'})
        self.fields['city'].widget.attrs.update({'class' : 'form-control'})
        self.fields['relationshipStatus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['kidsStatus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['hobbyList'].widget.attrs.update({'class' : 'form-control'})
        self.fields['partnerPreference'].widget.attrs.update({'class' : 'form-control'})
        self.fields['complexion'].widget.attrs.update({'class' : 'form-control'})
        self.fields['seekingRelationship'].widget.attrs.update({'class' : 'form-control'})
        self.fields['country'].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Profile
        fields = ['profile_pic','age', 'gender', 'seeking', 'about', 'state', 'city', 'relationshipStatus', 'kidsStatus', 'hobbyList', 'partnerPreference', 'complexion', 'seekingRelationship', 'country']

class SignUpStepOneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs.update({'class' : 'input100','placeholder' : 'Enter your age'})
        self.fields['relationshipStatus'].widget.attrs.update({'class' : 'form-control'})
        
   

    class Meta:
        model = Profile
        fields = ['age', 'relationshipStatus']

class SignUpStepTwoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class' : 'form-control'})
        self.fields['state'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your City'})
        self.fields['city'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your State'})
        self.fields['kidsStatus'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Kids Status'})
        self.fields['partnerPreference'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Partner Preference'})
        self.fields['complexion'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Complexion'})
        self.fields['seekingRelationship'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Select Seeking Realtionship'})
    class Meta:
        model = Profile
        fields = ['country', 'state','city', 'kidsStatus', 'partnerPreference', 'complexion', 'seekingRelationship']


class SignUpStepThreeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'class' : 'form-control'})
        self.fields['hobbyList'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Hobby List'})
        self.fields['about'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'About'})
    class Meta:
        model = Profile
        fields = ['profile_pic', 'hobbyList', 'about']



