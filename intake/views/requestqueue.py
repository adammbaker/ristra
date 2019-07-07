from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
    return redirect('request queue')

@site_admin_required
def organization_decline(request, queue_id):
    rq = RequestQueue.objects.get(id=queue_id)
    org = rq.organization
    org.delete()
    rq.delete()
    return redirect('request queue')
