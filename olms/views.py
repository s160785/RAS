from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import forms
from .models import UserProfile, Leaves

# Create your views here.


def main(response):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    return redirect('/home')


def newLeave(response):
    if not isinstance(response.user, User):
        return redirect('login')
    if response.method == 'GET':
        form = forms.newLeave()
        return render(response, 'newLeave.html', {'form': form})
    else:
        form = forms.newLeave(response.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = response.user.profile
            form.status = 'submitted'
            form.save()
        else:
            print('not valid')
        return redirect('home')


def home(response):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    leaves = Leaves.objects.filter(user=response.user.profile).order_by('-id')
    return render(response, 'home.html', {'leaves': leaves, 'id': response.user.profile.id})


def delete(response, lid):
    pass
