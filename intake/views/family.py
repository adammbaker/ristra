from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.forms.family import FamilyForm
from intake.models import Family, IntakeBus

# Create your views here.
class FamilyListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Family
    paginate_by = 0

    def get_queryset(self):
        return self.request.user.locations()

class FamilyCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Family
    parent = IntakeBus
    form_class = FamilyForm
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
        fam_family_name = form.cleaned_data.get('family_name')
        fam_intake_by = form.cleaned_data.get('intake_by')
        fam_lodging = form.cleaned_data.get('lodging')
        fam_destination_city = form.cleaned_data.get('destination_city')
        fam_state = form.cleaned_data.get('state')
        # if settings.DATABASE_REGIME == 'sqlite':
        #     fam_languages = ','.join(form.cleaned_data.get('languages'))
        # elif settings.DATABASE_REGIME == 'postgresql':
        #     fam_languages = form.cleaned_data.get('languages')
        fam_languages = form.cleaned_data.get('languages')
        print('FL', fam_languages, type(fam_languages), len(fam_languages))
        fam_days_traveling = form.cleaned_data.get('days_traveling')
        fam_days_detained = form.cleaned_data.get('days_detained')
        fam_country_of_origin = form.cleaned_data.get('country_of_origin')
        fam_notes = form.cleaned_data.get('notes')
        ib = get_object_or_404(IntakeBus, id=self.kwargs.get('ib_id'))
        fam, fam_c = Family.objects.get_or_create(
            family_name = fam_family_name,
            lodging = fam_lodging,
            destination_city = fam_destination_city,
            state = fam_state,
            days_traveling = fam_days_traveling,
            days_detained = fam_days_detained,
            country_of_origin = fam_country_of_origin,
        )
        fam.languages.set(fam_languages)
        fam.intake_by = fam_intake_by
        fam.notes = fam_notes
        ib.families.add(fam)
        ib.save()
        fam.save()
        # return to parent detail
        return redirect('intakebus:detail', ib_id = ib.id)

class FamilyDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Family

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['fam_id'])

class FamilyEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Family
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['fam_id'])







# @method_decorator([login_required], name='dispatch')
# class FamilyCreationView(LoginRequiredMixin, CreateView):
#     model = Family
#     form_class = FamilyForm
#     template_name = 'intake/family-add-form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'Family'
#         kwargs['intakebus'] = IntakeBus.objects.get(id=self.kwargs['ib_id'])
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         fam_family_name = form.cleaned_data['family_name']
#         fam_intake_by = form.cleaned_data['intake_by']
#         fam_lodging = form.cleaned_data['lodging']
#         fam_destination_city = form.cleaned_data['destination_city']
#         fam_state = form.cleaned_data['state']
#         fam_languages = form.cleaned_data['languages']
#         fam_days_traveling = form.cleaned_data['days_traveling']
#         fam_days_detained = form.cleaned_data['days_detained']
#         fam_country_of_origin = form.cleaned_data['country_of_origin']
#         fam_notes = form.cleaned_data['notes']
#         ib = get_object_or_404(IntakeBus, id=self.kwargs['ib_id'])
#         fam, fam_c = Family.objects.get_or_create(
#             family_name = fam_family_name,
#             intake_by = fam_intake_by,
#             lodging = fam_lodging,
#             destination_city = fam_destination_city,
#             state = fam_state,
#             languages = fam_languages,
#             days_traveling = fam_days_traveling,
#             days_detained = fam_days_detained,
#             country_of_origin = fam_country_of_origin,
#             notes = fam_notes
#         )
#         ib.families.add(fam)
#         ib.save()
#         print('------',fam)
#         print(fam.languages)
#         fam.save()
#         print('IB', ib, ib.id)
#         # return to parent detail
#         return redirect('intakebus:detail', ib_id = ib.id)
#
# class FamilyDetailView(LoginRequiredMixin, ListView):
#     'Shows the current Family and its children'
#     model = Family
#     context_object_name = 'fam'
#     ordering = ('-id', )
#     paginate_by = 0
#     template_name = 'intake/family-detail.html'
#
#     def get_queryset(self):
#         queryset = get_object_or_404(self.model, id=self.kwargs['fam_id'])
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = self.context_object_name
#         return context
