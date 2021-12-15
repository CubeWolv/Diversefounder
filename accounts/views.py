from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login
from decimal import Decimal
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from main.views import projects


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

 
@login_required
def dashboard(request):
    firstname = request.user.first_name
    lastname = request.user.last_name
    email=request.user.email
    return render(request, "dashboard.html",{'firstname': firstname,'lastname':lastname, 'email':email})


def login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect(projects)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        

        user = authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            return redirect('dashboard')

        else:
            messages.info(request, 'Invalid username or password')
            return redirect("login")
    if 'next' in request.POST:
        return redirect(request.POST['next'])

    return render(request, 'forms/login.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')





def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('forms/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'forms/signup.html', {'form': form, 'title':'reqister here'})
  