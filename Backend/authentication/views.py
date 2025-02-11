from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']

        #if User.objects.filter(username=username):
            #messages.error(request, "username already exists, please try something else")
            #return redirect('home')
        
        # if User.objects.filter(email=email):
           # messages.error(request, "email already exists, please login")
            #return redirect('signin')
        
        #if len(username)>15:
            #messages.error(request, "username is too long, please try something else")
           
        # if pass1 != pass2:
            # messages.error(request, "passwords do not match")
        
        #if not username.isalnum():
            #message.error(request, "username nust be alpha numeric")
            #return redirect('home')
      
        

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        messages.success(request, "account created succesfully")

        return redirect('signin')
    
    
    return render(request, 'authentication/register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
    
        if user is not None:
            login(request, user)
            fname= user.first_name
            return render(request,  'authentication/index.html',{'fname':fname})
        
        else:
            messages.error(request, "incorrect credentials")
            return redirect('home')
    
    return render(request, 'authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect('home')


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())
			form.save()

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ('home')
      
	form = ContactForm()
	return render(request, 'authentication/contact.html', {'form':form})




def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "authentication/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
			else:
			    messages.error(request,"please provide email for this account.")
			password_reset_form = PasswordResetForm()

	context={
		"password_reset_form":password_reset_form
		}

	return render(request, "authentication/password/password_reset.html", context)

@login_required
def profile(request):
	if request.method == 'POST':
		user_form = UpdateUserForm(request.POST, instance=request.user)
		profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile is updated successfully')
			return redirect(to='users-profile')
	else:
		user_form = UpdateUserForm(instance=request.user)
		profile_form = UpdateProfileForm(instance=request.user.profile)

	return render(request, 'authentication/profile.html', {'user_form': user_form, 'profile_form': profile_form})

