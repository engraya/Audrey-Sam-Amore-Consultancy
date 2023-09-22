from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Consultant, Client, Appointment, Message



# ADMIN REGISTRATION FORM
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


#Consultant related form
class ConsultantUserForm(forms.ModelForm):
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
        fields=['first_name','last_name','email', 'username','password']

class ConsultantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profilePicture'].widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model= Consultant
        fields=['profilePicture']

#Client User Form
class ClientUserForm(forms.ModelForm):
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
        model=User
        fields=['first_name','last_name','username','password']

class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profilePicture'].widget.attrs.update({'class' : 'form-control'})
        self.fields['gender'].widget.attrs.update({'class' : 'form-control'})
        self.fields['assignedConsultantID'].widget.attrs.update({'class' : 'form-control'})
    assignedConsultantID=forms.ModelChoiceField(queryset=Consultant.objects.all().filter(status=True),empty_label="Select Consultant", to_field_name="user_id")
    class Meta:
        model= Client
        fields=['profilePicture','gender']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})
        
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    consultantID=forms.ModelChoiceField(queryset=Consultant.objects.all().filter(status=True),empty_label="Consultant", to_field_name="user_id")
    clientID=forms.ModelChoiceField(queryset=Client.objects.all().filter(status=True),empty_label="Client", to_field_name="user_id")
    class Meta:
        model = Appointment
        fields = ['notes','description','category']



class MessageForm(forms.ModelForm):
    consultantID=forms.ModelChoiceField(queryset=Consultant.objects.all().filter(status=True),empty_label="Consultant", to_field_name="user_id")
    clientID=forms.ModelChoiceField(queryset=Client.objects.all().filter(status=True),empty_label="Client", to_field_name="user_id")
    class Meta:
        model = Message
        fields = ['content']


#for CONTACT US page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class AppointmentRequestForm(forms.Form):
    appointment_date = forms.DateTimeField(label='Appointment Date and Time', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    notes = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'rows': 4}))

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        # Add validation logic here if needed
        # For example, ensure the appointment date is in the future
        return appointment_date


class AppointmentResponseForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['notes']



