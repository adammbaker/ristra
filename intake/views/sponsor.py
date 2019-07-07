from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from intake.forms.sponsor import SponsorForm
from intake.models import Family, Sponsor

# Create your views here.
@method_decorator([login_required], name='dispatch')
class SponsorCreationView(LoginRequiredMixin, CreateView):
    model = Sponsor
    form_class = SponsorForm
    template_name = 'intake/sponsor-add-form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Sponsor'
        kwargs['family'] = Family.objects.get(id=self.kwargs['fam_id'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        sponsor_name = form.cleaned_data['name']
        sponsor_phone_number = form.cleaned_data['phone_number']
        sponsor_address = form.cleaned_data['address']
        sponsor_city = form.cleaned_data['city']
        sponsor_state = form.cleaned_data['state']
        sponsor_relation = form.cleaned_data['relation']
        sponsor_notes = form.cleaned_data['notes']
        fam = get_object_or_404(Family, id=self.kwargs['fam_id'])
        sponsor, sponsor_c = Sponsor.objects.get_or_create(
            name = sponsor_name,
            phone_number = sponsor_phone_number,
            address = sponsor_address,
            city = sponsor_city,
            state = sponsor_state,
            relation = sponsor_relation,
            notes = sponsor_notes,
        )
        print('FAM',fam.id, fam.family_name)
        fam.sponsor = sponsor
        fam.save()
        # return to parent detail
        print('Sending to faimly detail for', fam.id)
        return redirect('family:detail', fam_id = fam.id)

class SponsorDetailView(LoginRequiredMixin, ListView):
    'Shows the current Sponsor'
    model = Sponsor
    context_object_name = 'sponsor'
    ordering = ('-id', )
    paginate_by = 0
    template_name = 'intake/sponsor-detail.html'

    def get_queryset(self):
        queryset = get_object_or_404(self.model, id=self.kwargs['sponsor_id'])
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(self.__class__, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['active_view'] = self.context_object_name
        return context
