from django.contrib.auth import login
from django.views.generic import CreateView
from intake.forms.signup_forms import TeamLeadSignUpForm
from intake.models import User

# Create your views here.
class TeamLeadSignUpView(CreateView):
    model = User
    form_class = TeamLeadSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'team lead'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
