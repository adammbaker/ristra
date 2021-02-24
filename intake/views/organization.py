from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.decorators import sc_required
from intake.forms.organization import OrganizationForm
from intake.models import Organization, SiteCoordinator, RequestQueue, User

# Create your views here.
class OrganizationListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Organization
    paginate_by = 0

@method_decorator([login_required, sc_required], name='dispatch')
class OrganizationCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Organization
    parent = User
    form_class = OrganizationForm
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
        print('SC ID', self.request.user.id)
        # sc = SiteCoordinator.objects.get(user_id=self.request.user.id)
        sc = self.request.user.profile
        org_name = form.cleaned_data.get('name')
        org_city = form.cleaned_data.get('city')
        org_state = form.cleaned_data.get('state')
        org_url = form.cleaned_data.get('url')
        org_notes = form.cleaned_data.get('notes')
        org, org_c = Organization.objects.get_or_create(
            is_valid = False,
            name = org_name,
            city = org_city,
            state = org_state,
            url = org_url,
            notes = org_notes,
        )
        print('Setting up org', org.id, 'with sc as', sc)
        # sc.organization.add(Organization.objects.get(id=org.id))
        # sc.save()
        if sc.can_create_organization:
            sc.organizations_created.add(org)
            sc.affiliation = org
            sc.can_create_organization = False
            sc.save()
        else:
            return redirect('user:request permission')
        rq, rq_c = RequestQueue.objects.get_or_create(
            site_coordinator = sc,
            organization = org,
        )
        #TK email site admin
        subject_line = 'Organization Creation Request'
        body = []
        body.append('%(name)s (%(username)s) would like to set up an organization.' % {
            'name': sc.user.profile.name,
            'username': sc.user.username
        })
        body.append('%(org_name)s' % {'org_name': org.name})
        body.append('%(org_loc)s' % {'org_loc': org.location})
        body.append(f'\nPlease visit {get_current_site(self.request)}/requestqueue/')
        send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, ['adam.m.baker@gmail.com'], fail_silently=False)
        return redirect('organization:detail', org_id = org.id)

class OrganizationDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Organization

    def get_object(self, **kwargs):
        # return self.model.objects.get(id=self.kwargs.get('org_id'))
        return self.request.user.profile.affiliation
        return get_object_or_404(self.request.user.profile.affiliation)
        return get_object_or_404(self.model, id=self.kwargs.get('org_id'))

class OrganizationEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to edit the instance of an object'
    model = Organization
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs.get('org_id'))

class OrganizationUpdate(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name',]
    slug_url_kwarg = 'org_id'
    template_name = 'intake/generic-form.html'


# @method_decorator([login_required, sc_required], name='dispatch')
# class OrganizationCreationView(LoginRequiredMixin, CreateView):
#     model = Organization
#     form_class = OrganizationForm
#     template_name = 'intake/organization-add-form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'Organization'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         print('POC ID', self.request.user.id)
#         poc = SiteCoordinator.objects.get(user_id=self.request.user.id)
#         org_name = form.cleaned_data.get('name')
#         org_city = form.cleaned_data.get('city')
#         org_state = form.cleaned_data.get('state')
#         org_url = form.cleaned_data.get('url')
#         org_notes = form.cleaned_data.get('notes')
#         org, org_c = Organization.objects.get_or_create(
#             is_valid = False,
#             name = org_name,
#             city = org_city,
#             state = org_state,
#             url = org_url,
#             notes = org_notes,
#         )
#         print('Setting up org', org.id, 'with poc as', poc)
#         poc.organization = Organization.objects.get(id=org.id)
#         poc.save()
#         rq, rq_c = RequestQueue.objects.get_or_create(
#             point_of_contact = poc,
#             organization = org,
#         )
#         rq.save()
#         #TK email site admin
#         subject_line = 'Organization Creation Request'
#         body = []
#         body.append('%(name)s (%(username)s) would like to set up an organization.' % {
#             'name': poc.user.name,
#             'username': poc.user.username
#         })
#         body.append('%(org_name)s' % {'org_name': org.name})
#         body.append('%(org_loc)s' % {'org_loc': org.location})
#         body.append('\nPlease visit http://localhost:8000/requestqueue/')
#         send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, ['adam.m.baker@gmail.com'], fail_silently=False)
#         return redirect('organization:detail', org_id = org.id)
#
# class OrganizationDetailView(LoginRequiredMixin, ListView):
#     'Shows the current Organization and its children'
#     model = Organization
#     context_object_name = 'org'
#     ordering = ('-id', )
#     paginate_by = 0
#     template_name = 'intake/organization-detail.html'
#
#     def get_queryset(self):
#         queryset = get_object_or_404(self.model, id=self.kwargs['org_id'])
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = self.context_object_name
#         return context
#
# class OrganizationListView(LoginRequiredMixin, ListView):
#     'Shows the current Organizations in-scope'
#     model = Organization
#     paginate_by = 0
#     template_name = 'intake/organization-list.html'
#
#     def get_queryset(self):
#         # Customize the queryset to display in-scope items
#         queryset = self.request.user.organizations()
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = 'home'
#         return context
