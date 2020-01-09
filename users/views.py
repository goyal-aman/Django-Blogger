from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username    = form.cleaned_data.get('username')
            messages.success(request,f'{username} Registered')
            return redirect('users-login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', { 'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Updated')
            return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'p_form':p_form,
        'u_form':u_form
    }
    return render(request, 'users/profile.html', context)