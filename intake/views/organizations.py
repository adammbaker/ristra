from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template import loader
from django.views.generic.base import TemplateView

# from intake.encryption import Encryption
from datetime import datetime, timedelta
# from intake.forms.organizations import OrganizationForm
# from intake.generic_card import GenericCard
# from intake.models import Location, Organization, Volunteer
from shortener import shortener

from socket import gethostname, gethostbyname

@login_required
def organization_add(request):
    'Show organizations, or send to organization add if no Organizations'
    # if request.method =='POST' and request.user.has_perms(['intake.change_Organization', 'intake.delete_Organization', 'intake.add_Organization']):
    #     form = OrganizationForm(request.POST)
    #     if form.is_valid():
    #         org = form.save(commit=False)
    #         org.save()
    #         print('Saving organization:', Organization.objects.last())
    #         print(request.user.username, 'is being added to org')
    #         return redirect('families') #TK should redirect to bus add upon location add or possibly a landing page asking the user what they want to do
    # else:
    #     form = OrganizationForm()
    # return render(request, 'intake/organization-add.html', {'form': form})
    return HttpResponse('Organizaitons')

@login_required
def organization_affiliate(request, id, campaign):
    'Shows the page required to affiliate with an organization'
    # org = get_object_or_404(Organization, id=id)
    # vol = get_object_or_404(Volunteer, user__username=request.user.username)
    # if id == int(UrlMap.objects.get(short_url=campaign).full_url.split('/')[-2]):
    #     vol.affiliations.add(org)
    #     vol.campaigns.add(campaign)
    #     vol.save()
    # return HttpResponseRedirect(reverse('user overview'))
    # secret = request.GET.get('org_id')
    # print('CODE:', secret)
    # for org in Organization.objects.all():
    #     dec = Encryption(org.name)
    #     # print('DEC',dec.decode(secret))
    #     if dec.decode(secret) == str(org.id):
    #         print('Adding %(user)s to %(org)s' % {
    #             'user': request.user.username,
    #             'org': org.name
    #         })
    #         vol = get_object_or_404(Volunteer, user__username=request.user.username)
    #         vol.Organization.add(org)
    #         vol.save()
    # return HttpResponse('%(secret)s found' % {'secret': org.name})
    return HttpResponse('Organiazitons')

@login_required
def organization_overview(request, id):
    'Shows the information overview page for the requested organization'
    # print('ID',id,type(id))
    # org = get_object_or_404(Organization, id=id)
    # # org.obscure_code()
    # # print('CODE:',org.code)
    # template = loader.get_template('intake/organization-overview.html')
    # context = {
    #     'org': org,
    #     'qr_url': 'http://%(hn)s:8000/organizations/join/?org_id=%(enc)s' % {
    #         'hn': gethostbyname(gethostname()),
    #         'enc': org.code,
    #     }
    # }
    # return HttpResponse(template.render(context, request))
    return HttpResponse('Organizations')

# class OrganizationAddPageView(LoginRequiredMixin, TemplateView):
#     template_name = "intake/organization-add.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(OrganizationAddPageView, self).get_context_data(**kwargs)
#         context['form'] = OrganizationForm()
#         context['model'] = 'Organization'
#         messages.info(self.request, "hello org")
#         return context

@login_required
def organization_detail(request, id):
    'Shows the information overview page for the requested organization'
    # org = get_object_or_404(Organization, id=id)
    # template = loader.get_template('intake/organization-detail.html')
    # context = {
    #     'org': org,
    #     'url': 'http://www.ristra.com',
    #     'testvar': '<a href="">NN</a>'
    #     # 'qr_url': 'http://%(hn)s:8000/organization/join/?org_id=%(enc)s' % {
    #     #     'hn': gethostbyname(gethostname()),
    #     #     'enc': org.code,
    #     # }
    # }
    # return HttpResponse(template.render(context, request))
    return HttpResponse('Orgs')

@login_required
def organization_detail_fill(request, id):
    # org = Organization.objects.get(id=id)
    # if request.method =='POST' and request.user.has_perms(['intake.change_Organization', 'intake.delete_Organization', 'intake.add_Organization']):
    #     form = OrganizationForm(request.POST, instance=org)
    #     if form.is_valid():
    #         org = form.save(commit=False)
    #         org.save()
    #         print('Saving organization:', Organization.objects.last())
    #         print(request.user.username, 'is being added to org')
    #         return HttpResponseRedirect(reverse('org detail', kwargs={'id': org.id}))
    # else:
    #     form = OrganizationForm(instance=org)
    # return render(request, 'intake/organization-add.html', {'form': form})
    return HttpResponse('Orgs')

@login_required
def organization_detail_admin(request, id):
    'Allows a user with sufficient permissions to administer an organization page'
    # if request.user.has_perms(['intake.change_Organization', 'intake.delete_Organization', 'intake.add_Organization']):
    #     org = Organization.objects.get(id=id)
    #     gc = GenericCard()
    #     gc.body.title = 'Location'
    #     gc.body.buttons = ('success', '+')
    #     gc.footer.card_link = ('/location/add', 'Add New')
    #     template = loader.get_template('intake/organization-detail.html')
    #     context = {
    #         'org': org,
    #         'locations': Location.objects.filter(organization=org),
    #         'generic_card': gc,
    #     }
    #     return HttpResponse(template.render(context, request))
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return HttpResponse('Orgs')

@login_required
def organization_pubilicize(request, id):
    'Displays a page for the Point of Contact/a Deputy to print'
    # is_poc = Q(point_of_contact=request.user.Volunteer)
    # is_deputy = Q(deputies=request.user.Volunteer)
    # if Organization.objects.filter(is_poc | is_deputy).exists():
    #     org = get_object_or_404(Organization, id=id)
    #     short_url_base = 'http://localhost:8000/s/'
    #     short_url_slug = shortener.create(request.user, 'http://localhost:8000/organization/%(org_id)d/affiliate' % {
    #         'org_id': org.id,
    #     })
    #     short_url_slug = shortener.create(request.user, 'http://localhost:8000/organization/%(org_id)d/affiliate/%(slug)s' % {
    #         'org_id': org.id,
    #         'slug': short_url_slug,
    #     })
    #     short_url = short_url_base + short_url_slug
    #     template = loader.get_template('intake/organization-publicize.html')
    #     context = {
    #         'org': org,
    #         'short_url': short_url,
    #         'expiration_date': datetime.today() + timedelta(settings.SHORTENER_LIFESPAN // 86400),
    #         # 'url': shortener.shortener('https://www.ristrarefuge.com/organization/3/publicize')
    #     }
    #     return HttpResponse(template.render(context, request))
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return HttpResponse('Orgs')
    
