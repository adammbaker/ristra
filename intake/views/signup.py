from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from intake.forms import forms


def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.volunteers.name = form.cleaned_data.get('name')
            user.volunteers.email = form.cleaned_data.get('email')
            user.volunteers.phone_number = form.cleaned_data.get('phone_number')
            user.volunteers.languages.set(form.cleaned_data.get('languages'))
            user.volunteers.capacities.set(form.cleaned_data.get('capacities'))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = forms.SignUpForm()
    return render(request, 'intake/signup.html', {'form': form})
