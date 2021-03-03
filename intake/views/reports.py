from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.models import Asylee, HeadOfHousehold, Organization

from datetime import timedelta

# Create your views here.
class AtAGlance(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_ataglance.html'

    def get_object(self, **kwargs):
        return self.request.user.profile.affiliation

    def get_context_data(self, **kwargs):
        org = self.request.user.profile.affiliation
        # TOTAL EVER and TOTAL ACTIVE
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
        kwargs['ib_count'] = ib_count
        kwargs['hoh_count'] = hoh_count
        kwargs['asy_count'] = asy_count
        kwargs['loc_active_count'] = loc_active_count
        kwargs['ib_active_count'] = ib_active_count
        kwargs['hoh_active_count'] = hoh_active_count
        kwargs['asy_active_count'] = asy_active_count
        # HOUSEHOLDS LACKING
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
        # HOUSEHOLDS IN MOTION
        today = timezone.now()
        yesterday = today - timedelta(1)
        tomorrow = today + timedelta(1)
        overmorrow = today + timedelta(2)
        hohs_all = HeadOfHousehold.objects.filter(intakebus__location__organization=org)
        hoh_arr_yday = hohs_all.filter(
            intakebus__arrival_time__gte=yesterday,
            intakebus__arrival_time__lte=today,
        ).count()
        hoh_arr_today = hohs_all.filter(
            intakebus__arrival_time__gte=today,
            intakebus__arrival_time__lte=tomorrow,
        ).count()
        hoh_leaving_today = hohs_all.filter(
            travel_plan__city_van_date__gte=today,
            travel_plan__city_van_date__lte=tomorrow,
        ).count()
        hoh_leaving_tom = hohs_all.filter(
            travel_plan__city_van_date__gte=tomorrow,
            travel_plan__city_van_date__lte=overmorrow,
        ).count()
        kwargs['hohs_arr_yday'] = hoh_arr_yday
        kwargs['hohs_arr_today'] = hoh_arr_today
        kwargs['hohs_lvg_today'] = hoh_leaving_today
        kwargs['hohs_lvg_tom'] = hoh_leaving_tom
        return super().get_context_data(**kwargs)


class ActiveHouseholds(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_active_households.html'

    def get_object(self, **kwargs):
        return self.request.user.profile.affiliation

    def get_context_data(self, **kwargs):
        org = self.request.user.profile.affiliation
        active_hohs = [x for x in HeadOfHousehold.objects.filter(intakebus__location__organization=org).all() if x.is_active]
        kwargs['active_households'] = active_hohs
        return super().get_context_data(**kwargs)


class ActiveAsylees(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_active_asylees.html'

    def get_object(self, **kwargs):
        return self.request.user.profile.affiliation

    def get_context_data(self, **kwargs):
        org = self.request.user.profile.affiliation
        active_asys = [x for x in Asylee.objects.filter(head_of_household__intakebus__location__organization=org).order_by('head_of_household') if x.is_active]
        kwargs['active_asylees'] = active_asys
        return super().get_context_data(**kwargs)