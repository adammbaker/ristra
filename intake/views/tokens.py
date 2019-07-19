# from django.db.models import Q
# from django.db.utils import IntegrityError
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404, redirect, render, reverse
# from django.template import loader
# from django.utils import timezone
# from django.utils.decorators import method_decorator
# from django.views.generic import CreateView
# from django.views.generic.base import TemplateView
# from intake.decorators import site_admin_required
# from intake.forms.token_form import TokenForm
# from intake.models import Organization, PointOfContact, Token
#
# # from intake.encryption import Encryption
# from datetime import datetime, timedelta
# # from intake.forms.organizations import OrganizationForm
# # from intake.generic_card import GenericCard
# # from intake.models import Location, Organization, Volunteer
# from shortener import shortener
#
# from socket import gethostname, gethostbyname
#
# # Create your views here.
# # @method_decorator([login_required, site_admin_required], name='dispatch')
# # class OrganizationGenerationView(CreateView):
# #     model = Organization
# #     form_class = OrganizationValidateForm
# #     template_name = 'intake/organization-generate-form.html'
# #
# #     def get_context_data(self, **kwargs):
# #         kwargs['user_type'] = 'Organization'
# #         return super().get_context_data(**kwargs)
# #
# #     def get_initial(self):
# #         initial = super(OrganizationGenerationView, self).get_initial()
# #         initial = initial.copy()
# #         org = Organization.objects.filter(is_valid=False).last()
# #         initial['name'] = org.name
# #         initial['email'] =
# #         return initial
# #
# #     def form_valid(self, form):
# #         print('POC ID', self.request.user.id)
# #         poc = PointOfContact.objects.get(user_id=self.request.user.id)
# #         print('Validating org with poc as', poc)
# #         org = form.save()
# #         #TK email site admin
# #         #TK send to token request form
# #         return redirect('home')
#
# @site_admin_required
# def token_generate(request, poc_id):
#     'Generate a token to valid an organization'
#     if request.method =='POST':
#         print('POSTing')
#         form = TokenForm(request.POST)
#         print('FORMed', form.is_valid())
#         if form.is_valid():
#             token = form.save(commit=False)
#             print('Type', token, type(token))
#             print('TID', token.hash)
#             token = Token.objects.get(shorthash=token.hash)
#             token.notes = form.cleaned_data['notes']
#             token.save()
#             print('YY')
#             poc = PointOfContact.objects.get(user_id=token.reference_id)
#             # send an email to the Point Of Contact
#             subject_line = 'Organization Validation Token'
#             body = []
#             body.append('The site administrator has generated a token for you to use to validate %(org_name)s' % {
#                 'org_name': poc.organization.name
#             })
#             body.append('\nPlease visit http://localhost:8000/organization/validate/ and enter: %(hash)s' % {
#                 'hash': token.hash
#             })
#             body.append('\nRegards,\n\nSite Admin\nRistra Refuge')
#             send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, [poc.user.email], fail_silently=False)
#             return redirect('home')
#     else:
#         token = Token.objects.create()
#         print('new token created for %(pid)s' % {'pid': poc_id})
#         # try:
#         #     token = Token.objects.create()
#         #     print('new token created')
#         # except IntegrityError:
#         #     token = Token.objects.filter(max_uses__gt=0).last()
#         #     print('existing token found')
#         token.max_uses = 1
#         poc = PointOfContact.objects.get(user_id=poc_id)
#         token.reference_id = poc.user_id
#         token.save()
#         print(token.hash, token.creation_date, token.max_uses)
#         form = TokenForm(
#             initial={
#                 'poc': poc
#             }
#         )
#         # TK email the POC
#     return render(request, 'intake/token-generate-form.html', {'form': form, 'poc': poc})
