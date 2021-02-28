from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from intake.forms.sponsor import SponsorForm
from intake.models import HeadOfHousehold, Sponsor

# Create your views here.
class SponsorListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Sponsor
    paginate_by = 0

    def get_queryset(self):
        return HeadOfHousehold.objects.get(id=self.kwargs.get('hoh_id')).sponsor

class SponsorCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Sponsor
    parent = HeadOfHousehold
    form_class = SponsorForm
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Add %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Add a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        sponsor_name = form.cleaned_data.get('name')
        sponsor_phone_number = form.cleaned_data.get('phone_number')
        sponsor_address = form.cleaned_data.get('address')
        sponsor_city = form.cleaned_data.get('city')
        sponsor_state = form.cleaned_data.get('state')
        sponsor_relation = form.cleaned_data.get('relation')
        sponsor_notes = form.cleaned_data.get('notes')
        hoh = get_object_or_404(HeadOfHousehold, id=self.kwargs.get('hoh_id'))
        sponsor, sponsor_c = Sponsor.objects.get_or_create(
            name = sponsor_name,
            phone_number = sponsor_phone_number,
            address = sponsor_address,
            city = sponsor_city,
            state = sponsor_state,
            relation = sponsor_relation,
            notes = sponsor_notes,
        )
        hoh.sponsor = sponsor
        hoh.save()
        # return to parent overview
        print('Sending to faimly overview for', hoh.id)
        return redirect('headofhousehold:overview', hoh_id = hoh.id)

class SponsorDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Sponsor

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['spon_id'])

class SponsorEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Sponsor
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['spon_id'])



class SponsorUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = Sponsor
    parent = HeadOfHousehold
    # fields = '__all__'
    form_class = SponsorForm
    pk_url_kwarg = 'spon_id'
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Update %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Edit a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        # TK get logging in here for user
        return reverse_lazy('sponsor:detail', kwargs={'spon_id': self.kwargs.get('spon_id')})


class SponsorDelete(LoginRequiredMixin, DeleteView):
    model = Sponsor
    pk_url_kwarg = 'spon_id'
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        # TK get logging in here for user
        hoh_id = self.model.objects.get(id=self.kwargs.get('spon_id')).householdhead.id
        return reverse_lazy('headofhousehold:overview', kwargs={'hoh_id': hoh_id})
