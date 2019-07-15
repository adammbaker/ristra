from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from intake.forms.sponsor import SponsorForm
from intake.forms.travelplan import TravelPlanForm
from intake.models import Family, TravelPlan

# Create your views here.
@method_decorator([login_required], name='dispatch')
class TravelPlanCreationView(LoginRequiredMixin, CreateView):
    model = TravelPlan
    form_class = TravelPlanForm
    template_name = 'intake/travelplan-add-form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Travel Plan'
        kwargs['family'] = Family.objects.get(id=self.kwargs['fam_id'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        tp_arranged_by = form.cleaned_data['arranged_by']
        tp_confirmation = form.cleaned_data['confirmation']
        tp_destination_city = form.cleaned_data['destination_city']
        tp_destination_state = form.cleaned_data['destination_state']
        tp_travel_date = form.cleaned_data['travel_date']
        tp_city_van_date = form.cleaned_data['city_van_date']
        tp_travel_food_prepared = form.cleaned_data['travel_food_prepared']
        tp_eta = form.cleaned_data['eta']
        tp_travel_mode = form.cleaned_data['travel_mode']
        tp_notes = form.cleaned_data['notes']
        fam = get_object_or_404(Family, id=self.kwargs['fam_id'])
        tp, tp_c = TravelPlan.objects.get_or_create(
            arranged_by = tp_arranged_by,
            confirmation = tp_confirmation,
            destination_city = tp_destination_city,
            destination_state = tp_destination_state,
            travel_date = tp_travel_date,
            city_van_date = tp_city_van_date,
            travel_food_prepared = tp_travel_food_prepared,
            eta = tp_eta,
            travel_mode = tp_travel_mode,
            notes = tp_notes,
        )
        print('FAM',fam.id, fam.family_name)
        print('TPP', tp, tp.id, tp_c)
        fam.travel_plan = tp
        fam.save()
        # return to parent detail
        print('Sending to faimly detail for', fam.id)
        return redirect('family:detail', fam_id = fam.id)

class TravelPlanDetailView(LoginRequiredMixin, ListView):
    'Shows the current TravelPlan'
    model = TravelPlan
    context_object_name = 'tp'
    ordering = ('-id', )
    paginate_by = 0
    template_name = 'intake/travelplan-detail.html'

    def get_queryset(self):
        queryset = get_object_or_404(self.model, id=self.kwargs['tp_id'])
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(self.__class__, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['active_view'] = self.context_object_name
        return context
