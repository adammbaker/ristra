from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormView
from intake.forms.donate import DonateForm
from intake.models import Donate

# Create your views here.
class DonateList(ListView):
    'Lists all recipients of donations'
    model = Donate
    paginate_by = 0

    def get_context_data(self, **kwargs):
        kwargs['active_view'] = "donate"
        return super().get_context_data(**kwargs)


class DonateCreate(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Donate
    form_class = DonateForm
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Add %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Add a Recipient'
        kwargs['active_view'] = "donate"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        d_name = form.cleaned_data.get('name')
        d_location = form.cleaned_data.get('location')
        d_url = form.cleaned_data.get('url')
        d_description = form.cleaned_data.get('description')
        d, d_c = Donate.objects.get_or_create(
            name = d_name,
        )
        d.location = d_location
        d.url = d_url
        d.description = d_description
        d.save()
        # return to parent detail
        return redirect('donate:overview')

    def test_func(self):
        return self.request.user.is_superuser


class DonateDelete(LoginRequiredMixin, DeleteView):
    model = Donate
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('donate:overview')

    def test_func(self):
        return self.request.user.is_superuser


class DonateUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = Donate
    # fields = '__all__'
    form_class = DonateForm
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Update Donation Listing'
        kwargs['title'] = f"Edit Donation Listing"
        kwargs['active_view'] = "donate"
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        # TK get logging in here for user
        return reverse_lazy('donate:overview')

    def test_func(self):
        return self.request.user.is_superuser
