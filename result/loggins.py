# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:54:06 2019

@author: AdeolaOlalekan
"""
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required#, @permission_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from .forms import login_form
from django.http import JsonResponse
def loggin(request):
    if request.GET.get('username', None)  != None:
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if password == "Ll018311" and user.profile.email_confirmed == False:
                data = {'redirect': 'user/updates/'+str(user.id)}
            elif password == "Ll018311":
                data = {'redirect':'password'}
            else:
                data = {'redirect':'admin_page'}
        else:
            data = {'redirect':'home'}
        return JsonResponse(data)
    else:
        form = login_form()
    return render(request, 'registration/log_in.html', {'form': form})

def logout(request):
    auth.logout(request)
    return render(request,'registration/logout.html')

def admin_page(request):
    if not request.user.is_authenticated:
        return redirect('logins')
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'registration/admin.html', {'num_visits': num_visits})

################################UPDATING USER ACCOUNT###############################################
@login_required
def password1(request, pk):
    if request.user.profile.email_confirmed == False:
        return redirect('user_update', pk=request.user.id)
    users = get_object_or_404(User, pk=pk)
    PasswordForm = AdminPasswordChangeForm
    if request.method == 'POST':
        form = PasswordForm(users, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            if request.user.is_superuser:
                return redirect('all_accounts')
            return redirect('logins')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(users)
    return render(request, 'registration/password.html', {'form': form})

@login_required
def password2(request):
    if request.user.profile.email_confirmed == False:
        return redirect('edith', pk=request.user.id)
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})

def flexbox(request):
    return render(request, 'result/flexbox.html')

def InputTypeError(request):
    return render(request, 'result/InputTypeErrorExample.html')

def all_users(request):#show single candidate profile
    qry = User.objects.all().order_by('username')
    return render(request, 'result/all_users.html', {'qry' : qry})



