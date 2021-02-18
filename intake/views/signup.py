from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from intake.forms.signup import SignUpForm


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_site_coordinator:
            # return redirect('point_of_contact:home')
            return redirect('home')
        else:
            return redirect('home')
            # return redirect('intake:quiz_list')
    return render(request, 'intake/home.html')

from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from intake.forms.signup import ProfileForm   #, SignUpForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from intake.tokens import account_activation_token

# Sign Up View
class NewSignUpView(View):
    form_class = SignUpForm
    profile_form_class = ProfileForm
    template_name = 'intake/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        profile_form = self.profile_form_class()
        return render(request, self.template_name, {'form': form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Ristra account'
            message = render_to_string('intake/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            # return redirect('settings:profile')
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = SignUpForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#
# from django.contrib.auth import login, authenticate
# from django.shortcuts import render, redirect
# from intake.forms import forms
#
#
# def signup(request):
#     if request.method == 'POST':
#         form = forms.SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.volunteers.name = form.cleaned_data.get('name')
#             user.volunteers.email = form.cleaned_data.get('email')
#             user.volunteers.phone_number = form.cleaned_data.get('phone_number')
#             user.volunteers.languages.set(form.cleaned_data.get('languages'))
#             user.volunteers.capacities.set(form.cleaned_data.get('capacities'))
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = forms.SignUpForm()
#     return render(request, 'intake/signup.html', {'form': form})


from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from intake.tokens import account_activation_token

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')