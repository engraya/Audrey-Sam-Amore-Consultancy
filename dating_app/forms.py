from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Message, Client




class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Select Message Recipient'})
        self.fields['content'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter Message Cotent'})
    class Meta:
        model = Message
        fields = ['recipient','content', 'status']



class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter Appointment Description'})
        self.fields['category'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Select Appointment Category'})

    class Meta:
        model = Appointment
        fields = ['description', 'category','status']
