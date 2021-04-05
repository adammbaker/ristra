from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import User
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
        today = timezone.localtime(timezone.now()).date()
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
        hohs_departure_bags = hohs_all.filter(
            departure_bag_made=False,
            intakebus__location__organization=self.request.user.profile.affiliation,
        ).count()
        hohs_travel_food = hohs_all.filter(
            food_made=False,
            intakebus__location__organization=self.request.user.profile.affiliation,
        ).count()
        kwargs['hohs_arr_yday'] = hoh_arr_yday
        kwargs['hohs_arr_today'] = hoh_arr_today
        kwargs['hohs_lvg_today'] = hoh_leaving_today
        kwargs['hohs_lvg_tom'] = hoh_leaving_tom
        kwargs['hohs_departure_bags'] = hohs_departure_bags
        kwargs['hohs_travel_food'] = hohs_travel_food
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class ActiveHouseholds(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_active_households.html'

    def get_object(self, **kwargs):
        return self.request.user.profile.affiliation

    def get_context_data(self, **kwargs):
        org = self.request.user.profile.affiliation
        active_hohs = [x for x in HeadOfHousehold.objects.filter(intakebus__location__organization=org).order_by('intakebus__arrival_time') if x.is_active]
        sorted(active_hohs, key=lambda x: x.intakebus.arrival_time)
        kwargs['active_households'] = active_hohs
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class ActiveAsylees(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization
    template_name = 'intake/report_generic_asylees.html'

    def get_object(self, **kwargs):
        org = self.request.user.profile.affiliation
        unit_list = [x for x in Asylee.objects.filter(head_of_household__intakebus__location__organization=org).order_by('head_of_household__intakebus__arrival_time','head_of_household') if x.is_active]
        return sorted(unit_list, key=lambda x: x.householdhead.intakebus.arrival_time)

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Active Asylees'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsLackingTravelPlan(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS LACKING
        return HeadOfHousehold.objects.filter(
            travel_plan=None,
            intakebus__location__organization=self.request.user.profile.affiliation,
        )

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Lacking Travel Plan'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsLackingSponsor(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS LACKING
        return HeadOfHousehold.objects.filter(
            sponsor=None,
            intakebus__location__organization=self.request.user.profile.affiliation,
        )

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Lacking Sponsor'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class AsyleesLackingANumber(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = Asylee
    template_name = 'intake/report_generic_asylees.html'

    def get_object(self, **kwargs):
        no_a_num = Q(a_number=None) | Q(a_number='A-')
        affd_org = Q(
            head_of_household__intakebus__location__organization=self.request.user.profile.affiliation
        )
        return Asylee.objects.filter(
            no_a_num & affd_org
        )

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Asylees Lacking A-Numbers'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsArrivedYesterday(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS IN MOTION
        today = timezone.localtime(timezone.now()).date()
        yesterday = today - timedelta(1)
        hohs = HeadOfHousehold.objects.filter(
            intakebus__location__organization=self.request.user.profile.affiliation,
            intakebus__arrival_time__gte=yesterday,
            intakebus__arrival_time__lte=today,
        )
        return hohs

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Arrived Yesterday'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsArrivedToday(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS IN MOTION
        today = timezone.localtime(timezone.now()).date()
        tomorrow = today + timedelta(1)
        hohs = HeadOfHousehold.objects.filter(
            intakebus__location__organization=self.request.user.profile.affiliation,
            intakebus__arrival_time__gte=today,
            intakebus__arrival_time__lte=tomorrow,
        )
        return hohs

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Arrived Today'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsLeavingToday(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS IN MOTION
        today = timezone.localtime(timezone.now()).date()
        tomorrow = today + timedelta(1)
        hohs = HeadOfHousehold.objects.filter(
            intakebus__location__organization=self.request.user.profile.affiliation,
            travel_plan__city_van_date__gte=today,
            travel_plan__city_van_date__lte=tomorrow,
        )
        return hohs

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Leaving Today'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsLeavingTomorrow(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS IN MOTION
        today = timezone.localtime(timezone.now()).date()
        tomorrow = today + timedelta(1)
        overmorrow = today + timedelta(2)
        hohs = HeadOfHousehold.objects.filter(
            intakebus__location__organization=self.request.user.profile.affiliation,
            travel_plan__city_van_date__gte=tomorrow,
            travel_plan__city_van_date__lte=overmorrow,
        )
        return hohs

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Leaving Tomorrow'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class ReportSearch(LoginRequiredMixin, ListView):
    model = Asylee
    template_name = 'intake/report_list_asylees.html'

    def get_queryset(self, *args, **kwargs):
        sort_by = self.request.GET.get('sort_by', ['name', 'head_of_household__name','head_of_household__lodging','head_of_household__destination_state','head_of_household__intakebus__arrival_time','head_of_household__travel_plan__city_van_date','head_of_household__intakebus__number'])
        if isinstance(sort_by, str):
            if sort_by == 'asylee':
                sort_by = 'name'
            elif sort_by == '-asylee':
                sort_by = '-name'
            elif sort_by == 'household':
                sort_by = 'head_of_household__name'
            elif sort_by == '-household':
                sort_by = '-head_of_household__name'
            elif sort_by == 'lodging':
                sort_by = 'head_of_household__lodging'
            elif sort_by == '-lodging':
                sort_by = '-head_of_household__lodging'
            elif sort_by == 'arrival_time':
                sort_by = 'head_of_household__intakebus__arrival_time'
            elif sort_by == '-arrival_time':
                sort_by = '-head_of_household__intakebus__arrival_time'
            elif sort_by == 'departure':
                sort_by = 'head_of_household__travel_plan__city_van_date'
            elif sort_by == '-departure':
                sort_by = '-head_of_household__travel_plan__city_van_date'
            elif sort_by == 'bus':
                sort_by = 'head_of_household__intakebus__number'
            elif sort_by == '-bus':
                sort_by = '-head_of_household__intakebus__number'
            if sort_by in ('destination', '-destination'):
                sort_by = ['head_of_household__state', 'head_of_household__destination_city']
            else:
                sort_by = [sort_by]
        q_org = Q(head_of_household__intakebus__location__organization=self.request.user.profile.affiliation)
        q_active = Q(head_of_household__travel_plan=None) | Q(head_of_household__travel_plan__eta__gt=timezone.now() - timedelta(1))
        asys = self.model.objects.filter(
            q_org & q_active
        )
        # asys = self.model.objects.filter(
        #     head_of_household__intakebus__location__organization=self.request.user.profile.affiliation,
        #     head_of_household__travel_plan__eta__gt=timezone.now() - timedelta(1),
        # )
        return asys.order_by(*sort_by)

    def get_context_data(self, **kwargs):
        sort_by = self.request.GET.get('sort_by',None)
        desc = sort_by.startswith('-') if sort_by else False
        if desc:
            sort_by = sort_by[1:]
        fields = {'sorting': sort_by, 'ascending': not desc}
        kwargs['sorting'] = fields
        kwargs['destinations'] = sorted(set([x.householdhead.destination for x in Asylee.objects.filter(head_of_household__intakebus__location__organization=self.request.user.profile.affiliation)]))
        kwargs['active_view'] = 'search'
        kwargs['report_title'] = 'Search'
        return super().get_context_data(**kwargs)


class VolunteerSearch(LoginRequiredMixin, ListView):
    model = User
    template_name = 'intake/report_list_volunteers.html'

    def get_queryset(self, *args, **kwargs):
        sort_by = self.request.GET.get('sort_by', ['first_name','last_login','profile__role'])
        org = self.request.user.profile.affiliation
        users = User.objects.filter(
                profile__affiliation = org,
        )
        new_sort_by = sort_by
        if isinstance(sort_by, str):
            if sort_by == 'volunteer':
                new_sort_by = ['first_name']
            elif sort_by == '-volunteer':
                new_sort_by = ['-first_name']
            elif sort_by == 'lastlogin':
                new_sort_by = ['last_login']
            elif sort_by == '-lastlogin':
                new_sort_by = ['-last_login']
            elif sort_by == 'role':
                new_sort_by = ['role']
            elif sort_by == '-role':
                new_sort_by = ['-role']
            elif sort_by in ['clothing','concierge','departurebags','food','intake','medical','travel','transportation','volunteercoordinator']:
                has_capacity = Q(profile__capacities__name__icontains=sort_by)
                return users.filter(has_capacity)
            elif sort_by in ['-clothing','-concierge','-departurebags','-food','-intake','-medical','-travel','-transportation','-volunteercoordinator']:
                has_capacity = Q(profile__capacities__name__icontains=sort_by[1:])
                return users.filter(~has_capacity)
            else:
                new_sort_by = [sort_by]
        return users.order_by(*new_sort_by)

    def get_context_data(self, **kwargs):
        sort_by = self.request.GET.get('sort_by',None)
        desc = sort_by.startswith('-') if sort_by else False
        if desc:
            sort_by = sort_by[1:]
        fields = {'sorting': sort_by, 'ascending': not desc}
        kwargs['sorting'] = fields
        kwargs['active_view'] = 'search'
        kwargs['report_title'] = 'Volunteer Search'
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.profile.role in ('site_coordinator')


class HouseholdsLackingDepartureBags(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS LACKING
        return HeadOfHousehold.objects.filter(
            departure_bag_made=False,
            intakebus__location__organization=self.request.user.profile.affiliation,
        )

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Lacking Departure Bags'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)


class HouseholdsLackingTravelFood(LoginRequiredMixin, DetailView):
    'Details an instance of the objet'
    model = HeadOfHousehold
    template_name = 'intake/report_generic_households.html'

    def get_object(self, **kwargs):
        # HOUSEHOLDS LACKING
        return HeadOfHousehold.objects.filter(
            food_made=False,
            intakebus__location__organization=self.request.user.profile.affiliation,
        )

    def get_context_data(self, **kwargs):
        kwargs['report_title'] = 'Households Lacking Travel Food'
        kwargs['active_view'] = 'reports'
        return super().get_context_data(**kwargs)