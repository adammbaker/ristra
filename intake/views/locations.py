from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from intake.forms.locations import LocationForm
from intake.models import Locations

@login_required
def locations(request):
    'Show locations, or send to locations add if no Locations'
    if not Locations.objects.exists():
        if request.method =='POST':
            form = LocationForm(request.POST)
            if form.is_valid():
                loc = form.save(commit=False)
                loc.save()
                print('Saving location:', Locations.objects.last())
                return redirect('families') #TK should redirect to bus add upon location add or possibly a landing page asking the user what they want to do
                return HttpResponseRedirect('home')
        else:
            form = LocationForm()
        return render(request, 'intake/location-add.html', {'form': form})
        # return redirect('location add')
    return HttpResponse("This is what you see on the locations view and when there are locations.")

class LocationAddPageView(LoginRequiredMixin, TemplateView):
    template_name = "intake/location-add.html"

    def get_context_data(self, **kwargs):
        context = super(LocationAddPageView, self).get_context_data(**kwargs)
        context['form'] = LocationForm()
        context['model'] = 'Location'
        messages.info(self.request, "hello fam")
        return context
