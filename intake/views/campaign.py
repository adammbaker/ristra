from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from intake.decorators import poc_required
from intake.forms.campaign import CampaignForm
from intake.models import Campaign, Organization, PointOfContact, RequestQueue

# Create your views here.
@method_decorator([login_required, poc_required], name='dispatch')
class CampaignCreationView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'intake/campaign-add-form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Campaign'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print('POC ID', self.request.user.id)
        poc = PointOfContact.objects.get(user_id=self.request.user.id)
        org = form.save()
        print('Setting up org', org.id, 'with poc as', poc)
        poc.organization = Organization.objects.get(id=org.id)
        poc.save()
        rq, rq_c = RequestQueue.objects.get_or_create(
            point_of_contact = poc,
            organization = org,
        )
        rq.save()
        #TK email site admin
        subject_line = 'Organization Creation Request'
        body = []
        body.append('%(name)s (%(username)s) would like to set up an organization.' % {
            'name': poc.user.name,
            'username': poc.user.username
        })
        body.append('%(org_name)s' % {'org_name': org.name})
        body.append('%(org_loc)s' % {'org_loc': org.location})
        body.append('\nPlease visit http://localhost:8000/requestqueue/')
        send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, ['adam.m.baker@gmail.com'], fail_silently=False)
        return redirect('organization:detail', org_id = org.id)

@method_decorator([login_required, poc_required], name='dispatch')
class CampaignCreationView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'intake/campaign-add-form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Campaign'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        org_
        short_url = shortener.create(self.request.user, )
        print('POC ID', self.request.user.id)
        poc = PointOfContact.objects.get(user_id=self.request.user.id)
        org = form.save()
        print('Setting up org', org.id, 'with poc as', poc)
        poc.organization = Organization.objects.get(id=org.id)
        poc.save()
        rq, rq_c = RequestQueue.objects.get_or_create(
            point_of_contact = poc,
            organization = org,
        )
        rq.save()
        #TK email site admin
        subject_line = 'Organization Creation Request'
        body = []
        body.append('%(name)s (%(username)s) would like to set up an organization.' % {
            'name': poc.user.name,
            'username': poc.user.username
        })
        body.append('%(org_name)s' % {'org_name': org.name})
        body.append('%(org_loc)s' % {'org_loc': org.location})
        body.append('\nPlease visit http://localhost:8000/requestqueue/')
        send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, ['adam.m.baker@gmail.com'], fail_silently=False)
        return redirect('organization:detail', org_id = org.id)

def affiliate(request, org_hashid, short_url):
    'Affiliates the user to a campaign'
    pass
