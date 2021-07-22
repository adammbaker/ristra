from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

# from intake.forms import family
# from intake.forms import forms, family, intakebuses
from intake.decorators import site_admin_required
from intake.models import *

# Create your views here.
@site_admin_required
def request_queue(request):
    queues = RequestQueue.objects.all()
    template = loader.get_template('intake/request-queue.html')
    context = {
        'rqs': queues,
    }
    return HttpResponse(template.render(context, request))

@site_admin_required
def organization_approve(request, queue_id):
    rq = RequestQueue.objects.get(id=queue_id)
    org = rq.organization
    org.is_valid = True
    rq.delete()
    org.save()
    # Email user
    subject_line = 'Organization Approval Request'
    body = []
    body.append(f'Your request to approve {org.name} has been approved.')
    body.append('You may now proceed forward with your organization in Ristra Refuge.')
    send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, [org.organizations_created.first().user.email], fail_silently=False)
    return redirect('request queue')

@site_admin_required
def organization_decline(request, queue_id):
    rq = RequestQueue.objects.get(id=queue_id)
    org = rq.organization
    org.delete()
    rq.delete()
    # Email user
    subject_line = 'Organization Approval Request'
    body = []
    body.append(f'Your request to approve {org.name} has been declined.')
    body.append('If you feel this in error, please contact the site administrator at ristrarefuge@gmail.com.')
    send_mail(subject_line, '\n'.join(body), settings.EMAIL_FROM, [org.organizations_created.first().user.email], fail_silently=False)
    return redirect('request queue')
