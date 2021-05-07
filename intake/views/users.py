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

import logging

logger = logging.getLogger(__name__)

# Create your views here.
@login_required # TK SC perms required
def request_permission_to_create_organization(request):
    rq, rq_c = RequestQueue.objects.get_or_create(
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
    logger.info(f"Affiliating {user.username} to {org.name}")
    messages.success(request, f'You are now affiliated with {org.name}!')
    return redirect('home')

@login_required
def unaffiliate_user_from_organization(request):
    "Removes the user's affiliation to any organization"
    user = request.user
    org = user.profile.affiliation
    user.profile.affiliation = None
    user.save()
    logger.info(f"Removing {user.username}'s affiliation from {org.name}")
    messages.success(request, f"Your affiliation to {org.name} has been removed.")
    return redirect('home')

@login_required
def affiliate_to_other_organization(request, org_id):
    "Removes the user's affiliation and affiliates the user to another org"
    user = request.user
    old_org = user.profile.affiliation
    user.profile.affiliation = None
    user.save()
    org = Organization.objects.get(id=org_id)
    user.profile.affiliation = org
    user.save()
    logger.info(f"Removing {user.username}'s affiliation from {old_org.name} and affiliating {user.username} to {org.name}")
    messages.success(request, f"Your affiliation with {old_org.name} has been removed and replaced by an affiliation with {org.name}!")
    return redirect('home')