from django.contrib.auth import login
from django.views.generic import CreateView
from intake.forms.signup_forms import VolunteerSignUpForm
from intake.models import User

class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'volunteer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# @method_decorator([login_required], name='dispatch')
# class VolunteerCapacitiesView(UpdateView):
#     model = Student
#     form_class = StudentInterestsForm
#     template_name = 'classroom/students/interests_form.html'
#     success_url = reverse_lazy('students:quiz_list')
#
#     def get_object(self):
#         return self.request.user.student
#
#     def form_valid(self, form):
#         messages.success(self.request, 'Interests updated with success!')
#         return super().form_valid(form)
