from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Create your forms here.

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)

class UpdateUserForm(forms.ModelForm):
	username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
	
	class Meta:
		model = User
		fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
	avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
	bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

	class Meta:
		model = Profile
		fields = ['avatar', 'bio']