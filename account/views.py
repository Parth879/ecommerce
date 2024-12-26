from django.shortcuts import render,redirect
from account.forms import RegistrationForm
from account.models import Account
from django.contrib import auth
from django.contrib import messages

# Email
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


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

            context = {
                    'user':user,
                    'domain' : current_side,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : default_token_generator.make_token(user),
                }
            
            try:
                email_subject = "Please Activate Your Account."
                current_side = get_current_site(request)

                message = render_to_string('accounts/verfication_mail.html',context)
                send_email = EmailMessage(email_subject,message,to=[email])
                send_email.send()
            except:
                pass

            
            return redirect('/account/login/?command=verification&email='+email)
        else:
            
            messages.error(request,"User is already register")
            return redirect('/account/register/?&email='+email+'&uid='+context.uid)
            return register('register')
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
            messages.success(request,"Login Success.")
            return redirect('index')
        else:
            messages.success(request,"Login Again.")
            return redirect('login')

    
    return render(request,'accounts/login.html')


def activate(request,uid64,token):
    try:
        userid = urlsafe_base64_decode(uid64).decode()
        user = Account._default_manager.get(id=userid)
        tokens = default_token_generator.check_token(user,token)
    except:
        user = None
    
    if user is not None and tokens:
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
