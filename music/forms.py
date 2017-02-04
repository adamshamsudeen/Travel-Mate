from django import forms
from django.contrib.auth.models import User

from .models import Trip


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ['trip_source', 'trip_dest' , 'date' , 'vehicle' , 'amount']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
