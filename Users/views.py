from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from .functions import gene_errors
from .form import UserForm
from furniture.models import Customer

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                context = {
                    "title": "Login",
                    "error": True,
                    "message": "Invalid email or password"
                }
                return render(request, 'login.html', context=context)

    return render(request, 'login.html', {"title": "Login"})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = User.objects.create_user(
                username=instance.email,  # Assuming email is used as the username
                password=instance.password,
            )
            user = authenticate(request, username=instance.email, password=instance.password)
            Customer.objects.create(customer=user)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('furniture:index'))
        else:
            message = gene_errors(form)
            context = {
                'form': form,
                "error": True,
                "message": message
            }
            return render(request, 'signup.html', context=context)
    else:
        form = UserForm()
        context = {
            'form': form,
            "title": "Signup"
        }
    return render(request, 'signup.html', context=context)
