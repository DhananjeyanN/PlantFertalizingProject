from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import SiteProfile
from django.contrib import messages, auth

from accounts.forms import RegistrationForm, ProfileForm
from accounts.models import Profile


# Create your views here.

def register(request):
    profile = SiteProfile.objects.all().first()
    print(request.GET)
    if request.method == "POST":
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.password = request.POST.get('password')
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return redirect('login')

    else:
        form = RegistrationForm()

    context = {'profile': profile, 'form': form}
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))

            print('hello')
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Logged In!!!")
                return redirect('reg_index')
        else:
            messages.error(request, "Incorrect Login")
            return redirect('login')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context=context)


def logout(request):
    # profile = SiteProfile.objects.all().first()
    # context = {'profile':profile}
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged Out!!!')
    return redirect('login')


