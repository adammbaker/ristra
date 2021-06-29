from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from intake.forms.intakebus import IntakeBusForm
from intake.models import IntakeBus, Location

# Create your views here.
class IntakeBusListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = IntakeBus
    paginate_by = 0

    def get_queryset(self):
        return self.request.user.intakebuses()

class IntakeBusCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = IntakeBus
    parent = Location
    form_class = IntakeBusForm
    template_name = 'intake/generic-form.html'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        initial['arrival_time'] = timezone.now()
        return initial

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
        ib_origin = form.cleaned_data['origin']
        ib_state = form.cleaned_data['state']
        ib_arrival_time = form.cleaned_data['arrival_time']
        ib_number = form.cleaned_data['number']
        ib_notes = form.cleaned_data['notes']
        loc = get_object_or_404(Location, id=self.kwargs.get('loc_id'))
        ib, ib_c = IntakeBus.objects.get_or_create(
            origin = ib_origin,
            state = ib_state,
            arrival_time = ib_arrival_time
        )

        ib.number = ib_number
        ib.notes = ib_notes
        ib.save()
        loc.intakebuses.add(ib)
        loc.save()
        # return to parent detail
        return redirect('intakebus:overview', ib_id = ib.id)

class IntakeBusDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = IntakeBus

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['ib_id'])

class IntakeBusEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = IntakeBus
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['ib_id'])



class IntakeBusOverview(LoginRequiredMixin, DetailView):
    model = IntakeBus
    pk_url_kwarg = 'ib_id'
    template_name = 'intake/intakebus_overview.html'

    def get_context_data(self, **kwargs):
        kwargs['lod'] = 'partial'
        return super().get_context_data(**kwargs)


class IntakeBusDetail(LoginRequiredMixin, DetailView):
    model = IntakeBus
    pk_url_kwarg = 'ib_id'


class IntakeBusList(LoginRequiredMixin, ListView):
    model = IntakeBus
    pk_url_kwarg = 'ib_id'


class IntakeBusUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = IntakeBus
    parent = Location
    # fields = '__all__'
    form_class = IntakeBusForm
    pk_url_kwarg = 'ib_id'
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
        return redirect('intakebus:detail', kwargs={'ib_id': self.kwargs.get('ib_id')})


class IntakeBusDelete(LoginRequiredMixin, DeleteView):
    model = IntakeBus
    pk_url_kwarg = 'ib_id'
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        # TK get logging in here for user
        loc_id = self.model.objects.get(id=self.kwargs.get('ib_id')).location.id
        return redirect('location:overview', kwargs={'loc_id': loc_id})
