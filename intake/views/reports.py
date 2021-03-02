from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.models import Organization

# Create your views here.
class ReportAtAGlance(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_ataglance.html'

    def get_object(self, **kwargs):
        return self.request.user.profile.affiliation

    def get_context_data(self, **kwargs):
        ib_count = 0
        hoh_count = 0
        asy_count = 0
        loc_active_count = 0
        ib_active_count = 0
        hoh_active_count = 0
        asy_active_count = 0
        for location in self.request.user.profile.affiliation.locations.all():
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
        kwargs['ib_count'] = ib_count
        kwargs['hoh_count'] = hoh_count
        kwargs['asy_count'] = asy_count
        kwargs['loc_active_count'] = loc_active_count
        kwargs['ib_active_count'] = ib_active_count
        kwargs['hoh_active_count'] = hoh_active_count
        kwargs['asy_active_count'] = asy_active_count
        return super().get_context_data(**kwargs)