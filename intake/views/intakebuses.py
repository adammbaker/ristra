from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from intake.forms.intakebuses import IntakeBusForm
from intake.models import IntakeBuses, Location

@login_required
def intake_buses(request):
    'Show intake buses, or send to locations landing page if no Locations'
    if not Locations.objects.exists():
        return redirect('locations')
    if request.method =='POST':
        form = IntakeBusForm(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.save()
            print('Saving bus:', IntakeBuses.objects.last())
            return redirect('families') #TK should redirect to bus add upon location add or possibly a landing page asking the user what they want to do
            return HttpResponseRedirect('home')
    else:
        form = IntakeBusForm()
    return render(request, 'intake/intakebus-add.html', {'form': form})
    return HttpResponse("This is what you see on the intake buses view and when there are locations.")

class IntakeBusAddPageView(LoginRequiredMixin, TemplateView):
    template_name = "intake/family-add.html"

    def get_context_data(self, **kwargs):
        context = super(IntakeBusAddPageView, self).get_context_data(**kwargs)
        context['form'] = IntakeBusForm()
        context['model'] = 'Intake Bus'
        messages.info(self.request, "hello fam")
        return context
