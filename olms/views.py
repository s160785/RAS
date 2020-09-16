from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import forms
from .models import UserProfile, Leaves
from datetime import datetime

# Create your views here.


def main(response):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    return redirect('/home')


def register(response):
    if response.method == 'GET':
        return render(response, 'register.html', {'form': forms.student(), 'pform': forms.pform()})

    if response.method == 'POST':
        form = forms.student(response.POST)
        pform = forms.pform(response.POST)

        if pform.is_valid():
            cd = form.cleaned_data
            email = f'{cd["id"]}@rguktsklm.ac.in'
            user = User.objects.get_or_create(
                username=cd["username"], email=email)[0]
            user.set_password(cd["password1"])
            user.save()
            up = UserProfile(user=user)
            up.uid = cd['id'].capitalize()
            up.branch = cd['branch']
            up.year = cd['year']
            up.save()
            pform = pform.save(commit=False)
            pform.userprofile = up
            pform.save()

            return redirect('/')
        return render(response, 'register.html', {'form': form, 'pform': pform})


def userhome(response):
    if response.user.profile.usertype == 'admin':
        return redirect('admin_home')
    elif response.user.profile.usertype == 'security':
        return redirect('sec_home')
    return


def usertype(response):
    if response.user.profile.usertype == 'admin':
        return 'admin'
    elif response.user.profile.usertype == 'security':
        return 'security'
    return 'student'


def newLeave(response):
    if not isinstance(response.user, User):
        return redirect('login')
    if not usertype(response) == 'student':
        return redirect('home')
    if response.method == 'GET':
        form = forms.newLeave()
        if not response.user.profile.in_campus:
            return redirect('home')
        return render(response, 'newLeave.html', {'form': form})
    else:
        form = forms.newLeave(response.POST,  response.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = response.user.profile
            form.status = 'pending'
            form.save()
        else:
            return render(response, 'newLeave.html', {'form': form})
        return redirect('home')


def home(response):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if userhome(response):
        return redirect(userhome(response).url)
    if not response.user.profile.in_campus:
        return redirect('nic')
    leaves = Leaves.objects.filter(user=response.user.profile).order_by('-id')
    return render(response, 'home.html', {'leaves': leaves, 'id': response.user.profile.uid})


def delete(response, lid):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if not Leaves.objects.get(id=lid).user == response.user.profile:
        return redirect('home')
    try:
        Leaves.objects.get(id=lid).delete()
    except:
        return redirect('home')
    return redirect('home')


def admin_home(response):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'admin':
        return redirect('home')
    leaves = Leaves.objects.filter(
        user__year=response.user.profile.year).order_by('id')
    leaves = [l for l in leaves if l.status == 'pending']
    return render(response, 'admin_home.html', {'leaves': leaves, 'username': response.user.username})


def approve(response, lid):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'admin':
        return redirect('home')
    leave = Leaves.objects.get(id=lid)
    leave.status = 'granted'
    leave.save()
    return redirect('admin_home')


def reject(response, lid):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'admin':
        return redirect('home')
    leave = Leaves.objects.get(id=lid)
    leave.status = 'rejected'
    leave.save()
    return redirect('admin_home')


def sec_home(response):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'security':
        return redirect('home')
    leaves = Leaves.objects.filter(status__in=['granted', 'on_leave'])
    return render(response, 'sec_home.html', {'leaves': leaves})


def out(response, lid):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'security':
        return redirect('home')
    leave = Leaves.objects.get(pk=lid)
    leave.status = 'on_leave'
    leave.actual_out_date = datetime.now()
    leave.save()
    user = UserProfile.objects.get(uid=leave.user.uid)
    user.in_campus = False
    user.save()
    print(user)
    return redirect('sec_home')


def inn(response, lid):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'security':
        return redirect('home')
    leave = Leaves.objects.get(pk=lid)
    leave.status = 'completed'
    leave.actual_in_date = datetime.now()
    leave.save()
    user = UserProfile.objects.get(uid=leave.user.uid)
    user.in_campus = True
    user.save()
    return redirect('sec_home')


def leave_view(response, lid):
    if response.user.is_superuser or not isinstance(response.user, User):
        return redirect('logout')
    if usertype(response) != 'admin':
        return redirect('home')
    leave = Leaves.objects.get(pk=lid)
    return render(response, 'leave_view.html', {'leave': leave})


def nic(response):
    return render(response, 'nic.html', {})
