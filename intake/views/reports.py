from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.models import Asylee, HeadOfHousehold, Organization

# Create your views here.
class ReportAtAGlance(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_ataglance.html'

    def get_object(self, **kwargs):
        return self.request.user.profile.affiliation

    def get_context_data(self, **kwargs):
        org = self.request.user.profile.affiliation
        ib_count = 0
        hoh_count = 0
        asy_count = 0
        loc_active_count = 0
        ib_active_count = 0
        hoh_active_count = 0
        asy_active_count = 0
        for location in org.locations.all():
            loc_active_count += location.is_active
            ib_count += location.intakebuses.count()
            for bus in location.intakebuses.all():
                ib_active_count += bus.is_active
                hoh_count += bus.headsofhousehold.count()
                for hoh in bus.headsofhousehold.all():
                    hoh_active_count += hoh.is_active
                    asy_count += hoh.asylees.count()
                    for asy in hoh.asylees.all():
                        asy_active_count += asy.is_active
        kwargs['hoh_no_tp'] = HeadOfHousehold.objects.filter(
            travel_plan=None,
            intakebus__location__organization=org,
        ).count()
        kwargs['hoh_no_spon'] = HeadOfHousehold.objects.filter(
            sponsor=None,
            intakebus__location__organization=org,
        ).count()
        no_a_num = Q(a_number=None) | Q(a_number='A-')
        affd_org = Q(head_of_household__intakebus__location__organization=org)
        kwargs['asy_no_a_anum'] = Asylee.objects.filter(
            no_a_num & affd_org
        ).count()
        kwargs['ib_count'] = ib_count
        kwargs['hoh_count'] = hoh_count
        kwargs['asy_count'] = asy_count
        kwargs['loc_active_count'] = loc_active_count
        kwargs['ib_active_count'] = ib_active_count
        kwargs['hoh_active_count'] = hoh_active_count
        kwargs['asy_active_count'] = asy_active_count
        return super().get_context_data(**kwargs)