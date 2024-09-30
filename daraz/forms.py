from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = '__all__'
