from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.base import TemplateView
from intake.forms.signup import ProfileForm, SignUpForm
# from intake.forms.signup import NewSignUpForm, ProfileForm, SignUpForm, UserForm
from intake.models import Profile, User
from intake.templatetags.my_tags import to_phone_number
from intake.tokens import account_activation_token

# Create your views here.
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

class SignUpView(CreateView):
    form_class = SignUpForm
    profile_form_class = ProfileForm
    template_name = 'intake/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        profile_form = self.profile_form_class()
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # profile_form = self.profile_form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            profile = Profile.objects.get(user=user)
            # profile.name = form.cleaned_data.get('name')
            profile.languages.set(form.cleaned_data.get('languages'))
            profile.capacities.set(form.cleaned_data.get('capacities'))
            profile.role = form.cleaned_data.get('role')
            profile.phone_number = to_phone_number(form.cleaned_data.get('phone_number'))
            profile.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Ristra account'
            message = render_to_string('intake/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please confirm your email address by visiting the link we sent.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})
        # return render(request, self.template_name, {'form': form, 'profile_form': profile_form})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print(profile_form.cleaned_data.keys())
            print(profile_form.cleaned_data.get('role','Nonee'))
            messages.success(request, _('Your profile was successfully updated!'))
            # return redirect('settings:profile')
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = SignUpForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        print(profile_form.cleaned_data.keys())
        print(profile_form.cleaned_data.get('role','Nonee'))
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# class SignUpView(CreateView):
#     form_class = NewSignUpForm
#     success_url = reverse_lazy('login')
#     template_name = 'intake/signup.html'

# class ProfileUpdateView(LoginRequiredMixin, TemplateView):
#     user_form = UserForm
#     profile_form = ProfileForm
#     template_name = 'intake/signup.html'

#     def post(self, request):
#         post_data = request.POST

#         user_form = UserForm(post_data, instance=request.user)
#         profile_form = ProfileForm(post_data, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile was successfully updated!')
#             return HttpResponseRedirect(reverse_lazy('home'))
#             #TK

#         context = self.get_context_data(
#             user_form=user_form,
#             profile_form=profile_form
#         )

#         return self.render_to_response(context)     

#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

def update_user_profile(request):
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

class ProfileEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Profile
    template_name = 'intake/generic-form.html'
    fields = ['name','role','phone_number','languages','capacities',]

    def get_success_url(self):
        return reverse('user:update profile')

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Save Changes'
        kwargs['title'] = 'Edit profile'
        return super().get_context_data(**kwargs)

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(self.__class__, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['languages'] = self.request.user.profile.languages.all()
        initial['capacities'] = self.request.user.profile.capacities.all()
        return initial

    def get_object(self, **kwargs):
        user_id = self.request.user.id
        return self.model.objects.get(user__id=user_id)

class ProfileFormView(LoginRequiredMixin, FormView):
    template_name = 'intake/generic-form.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('user:update profile')

    def get_context_data(self, **kwargs):
        kwargs = super(ProfileFormView, self).get_form_kwargs()
        kwargs['button_text'] = 'Save Changes'
        kwargs['title'] = 'Edit profile'
        return super().get_context_data(**kwargs)

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(self.__class__, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # initial['name'] = self.request.user.profile.name
        initial['phone_number'] = self.request.user.profile.phone_number
        initial['languages'] = self.request.user.profile.languages.all()
        initial['capacities'] = self.request.user.profile.capacities.all()
        initial['role'] = self.request.user.profile.role
        return initial

    def form_valid(self, form):
        # up_name = form.cleaned_data.get('name')
        up_phone_number = form.cleaned_data.get('phone_number')
        up_languages = form.cleaned_data.get('languages')
        up_capacities = form.cleaned_data.get('capacities')
        up_role = form.cleaned_data.get('role')
        user = User.objects.get(id = self.request.user.id)
        # user.profile.name = up_name
        user.profile.phone_number = up_phone_number
        user.profile.languages.set(up_languages)
        user.profile.capacities.set(up_capacities)
        user.profile.role = up_role
        user.save()
        messages.success(self.request, ('Your profile was successfully updated!'))
        return redirect('user:update profile')

# class LocationEditView(LoginRequiredMixin, UpdateView):
#     'Allows a privileged user to to edit the instance of an object'
#     model = Location
#     template_name = 'intake/generic-form.html'

#     def get_object(self, **kwargs):
#         return self.model.objects.get(id=self.kwargs['loc_id'])

# def register(request):
#     if request.method == 'POST':
#         f = CustomUserCreationForm(request.POST)
#         if f.is_valid():
#             f.save()
#             messages.success(request, 'Account created successfully')
#             return redirect('register')

#     else:
#         f = CustomUserCreationForm()

#     return render(request, 'cadmin/register.html', {'form': f})