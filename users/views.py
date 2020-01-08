from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username    = form.cleaned_data.get('username')
            messages.success(request,f'{username} Registered')
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', { 'form':form})