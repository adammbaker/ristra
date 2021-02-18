from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
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
        # return to parent detail
        print('Sending to faimly detail for', hoh.id)
        return redirect('headofhousehold:detail', hoh_id = hoh.id)

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








# @method_decorator([login_required], name='dispatch')
# class SponsorCreationView(LoginRequiredMixin, CreateView):
#     model = Sponsor
#     form_class = SponsorForm
#     template_name = 'intake/sponsor-add-form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'Sponsor'
#         kwargs['family'] = Family.objects.get(id=self.kwargs['fam_id'])
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         sponsor_name = form.cleaned_data['name']
#         sponsor_phone_number = form.cleaned_data['phone_number']
#         sponsor_address = form.cleaned_data['address']
#         sponsor_city = form.cleaned_data['city']
#         sponsor_state = form.cleaned_data['state']
#         sponsor_relation = form.cleaned_data['relation']
#         sponsor_notes = form.cleaned_data['notes']
#         fam = get_object_or_404(Family, id=self.kwargs['fam_id'])
#         sponsor, sponsor_c = Sponsor.objects.get_or_create(
#             name = sponsor_name,
#             phone_number = sponsor_phone_number,
#             address = sponsor_address,
#             city = sponsor_city,
#             state = sponsor_state,
#             relation = sponsor_relation,
#             notes = sponsor_notes,
#         )
#         print('FAM',fam.id, fam.family_name)
#         fam.sponsor = sponsor
#         fam.save()
#         # return to parent detail
#         print('Sending to faimly detail for', fam.id)
#         return redirect('family:detail', fam_id = fam.id)
#
# class SponsorDetailView(LoginRequiredMixin, ListView):
#     'Shows the current Sponsor'
#     model = Sponsor
#     context_object_name = 'sponsor'
#     ordering = ('-id', )
#     paginate_by = 0
#     template_name = 'intake/sponsor-detail.html'
#
#     def get_queryset(self):
#         queryset = get_object_or_404(self.model, id=self.kwargs['sponsor_id'])
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = self.context_object_name
#         return context
