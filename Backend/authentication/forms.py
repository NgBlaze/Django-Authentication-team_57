from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Contact


# Create your forms here

class ContactForm(ModelForm):
	class Meta:
		model = Contact
		fields = ['first_name', 'last_name', 'email_address', 'message']

		

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs.update({'class': 'contact-us__input-box'})


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