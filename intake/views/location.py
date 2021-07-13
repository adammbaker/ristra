from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from intake.decorators import sc_required, team_lead_required
from intake.forms.location import LocationForm
from intake.models import Location, Organization

# Create your views here.
class LocationListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Location
    paginate_by = 0

    def get_queryset(self):
        return self.request.user.locations()

class LocationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Location
    parent = Organization
    form_class = LocationForm
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        print('GCD 1')
        kwargs['button_text'] = 'Add %(model)s' % {
            'model': self.model.__name__
        }
        print('GCD 2')
        kwargs['title'] = 'Add a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        print('GCD 3')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print('FV 1')
        loc_name = form.cleaned_data.get('name')
        loc_notes = form.cleaned_data.get('notes')
        print('FV 2')
        org = get_object_or_404(Organization, id=self.kwargs.get('org_id'))
        print('FV 3')
        loc, loc_c = Location.objects.get_or_create(
            name = loc_name,
        )
        loc.notes = loc_notes
        print('FV 4')
        loc.save()
        print('FV 5')
        org.locations.add(loc)
        print('FV 6')
        org.save()
        print('FV 7')
        # return to parent detail
        return redirect('location:overview', loc_id=loc.id)

    def test_func(self):
        print('TF 1')
        return self.request.user.profile.role in ('site_coordinator','team_lead')


# class LocationDetailView(LoginRequiredMixin, DetailView):
#     'Details an instance of the object'
#     model = Location

#     def get_object(self, **kwargs):
#         return self.model.objects.get(id=self.kwargs['loc_id'])


class LocationOverview(LoginRequiredMixin, DetailView):
    model = Location
    pk_url_kwarg = 'loc_id'
    template_name = 'intake/location_overview.html'

    def get_context_data(self, **kwargs):
        kwargs['lod'] = 'partial'
        return super().get_context_data(**kwargs)


class LocationDetail(LoginRequiredMixin, DetailView):
    model = Location
    pk_url_kwarg = 'loc_id'


class LocationList(LoginRequiredMixin, ListView):
    model = Organization
    pk_url_kwarg = 'org_id'
    template_name = 'intake/organization_list.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs.get('org_id'))


class LocationUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = Location
    parent = Organization
    # fields = '__all__'
    form_class = LocationForm
    pk_url_kwarg = 'loc_id'
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
        return redirect('location:detail', loc_id=self.kwargs.get('loc_id'))


class LocationDelete(LoginRequiredMixin, DeleteView):
    model = Location
    pk_url_kwarg = 'loc_id'
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        # TK get logging in here for user
        org_id = self.model.objects.get(id=self.kwargs.get('loc_id')).organization.id
        return redirect('organization:overview', org_id=org_id)
