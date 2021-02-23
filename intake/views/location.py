from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.decorators import sc_required
from intake.forms.location import LocationForm
from intake.models import Location, Organization

# Create your views here.
class LocationListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Location
    paginate_by = 0

    def get_queryset(self):
        return self.request.user.locations()

@method_decorator([login_required, sc_required], name='dispatch')
class LocationCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Location
    parent = Organization
    form_class = LocationForm
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
        loc_name = form.cleaned_data.get('name')
        loc_notes = form.cleaned_data.get('notes')
        org = get_object_or_404(Organization, id=self.kwargs.get('org_id'))
        loc, loc_c = Location.objects.get_or_create(
            name = loc_name,
            notes = loc_notes,
        )
        org.locations.add(loc)
        org.save()
        # return to parent detail
        return redirect('location:detail', loc_id = loc.id)

class LocationDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Location

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['loc_id'])

class LocationEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Location
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['loc_id'])





# @method_decorator([login_required], name='dispatch')
# class LocationCreationView(LoginRequiredMixin, CreateView):
#     model = Location
#     form_class = LocationForm
#     template_name = 'intake/location-add-form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'Location'
#         print('KEYS',self.kwargs.keys())
#         kwargs['organization'] = Organization.objects.get(id=self.kwargs['org_id'])
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         loc_name = form.cleaned_data['name']
#         loc_notes = form.cleaned_data['notes']
#         org = get_object_or_404(Organization, id=self.kwargs['org_id'])
#         loc, loc_c = Location.objects.get_or_create(
#             name = loc_name,
#             notes = loc_notes,
#         )
#         org.locations.add(loc)
#         org.save()
#         # return to parent detail
#         return redirect('organization:detail', org_id = loc.organization.id)
#
# class LocationDetailView(LoginRequiredMixin, ListView):
#     'Shows the current Location and its children'
#     model = Location
#     context_object_name = 'loc'
#     ordering = ('-id', )
#     paginate_by = 0
#     template_name = 'intake/location-detail.html'
#
#     def get_queryset(self):
#         queryset = get_object_or_404(self.model, id=self.kwargs['loc_id'])
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = self.context_object_name
#         return context
#
# class LocationListView(LoginRequiredMixin, ListView):
#     'Shows the current Locations in-scope'
#     model = Location
#     paginate_by = 0
#     template_name = 'intake/location-list.html'
#
#     def get_queryset(self):
#         # Customize the queryset to display in-scope items
#         print('LOCID',self.kwargs.get('loc_id'))
#         queryset = self.request.user.locations(Organization.objects.get(id=self.kwargs.get('loc_id')))
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = self.model.__class__.__name__
#         return context
#
# class LocationUpdateView(UpdateView):
#     model = Location
#     fields = ['name','lodging_type','notes',]
#     template_name = 'intake/location-edit-form.html'
#
#     def get_object(self, **kwargs):
#         return self.model.objects.get(id=self.kwargs['loc_id'])
