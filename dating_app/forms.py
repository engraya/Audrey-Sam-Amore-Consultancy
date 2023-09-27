from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Message




class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'category']
