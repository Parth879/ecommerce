from django.shortcuts import render,redirect
from account.forms import RegistrationForm
from account.models import Account
from django.contrib import auth
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data.get('email')
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number = phone_number
            user.save()
            return redirect('index')
        
    else:
        form = RegistrationForm()

    context = {
        'form':form,
    }
    return render(request,'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']

        user = auth.authenticate(request,username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        
    return render(request,'accounts/login.html')