from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from intake.decorators import site_admin_required
from intake.models import Organization, RequestQueue

# Create your views here.
@login_required # TK SC perms required
def request_permission_to_create_organization(request):
    rq = RequestQueue.objects.create(
        site_coordinator = request.user.profile,
    )
    message = ('primary', 'Your request for permission to create an organization has been received and will be considered shortly.')
    request.session['message'] = message
    return redirect('home')

@site_admin_required
def approve_organization_creation(request, queue_id):
    rq = RequestQueue.objects.get(id=queue_id)
    user = rq.site_coordinator
    user.can_create_organization = True
    user.save()
    rq.delete()
    return redirect('request queue')

@site_admin_required
def decline_organization_creation(request, queue_id):
    rq = RequestQueue.objects.get(id=queue_id)
    rq.delete()
    return redirect('request queue')

@login_required
def affiliate_user_to_organization(request, org_id):
    'Affiliates a user to an organization'
    org = Organization.objects.get(id=org_id)
    user = request.user
    user.profile.affiliation = org
    user.save()
    return redirect('home')