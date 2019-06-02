from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from intake.forms.family import FamilyForm
from intake.models import IntakeBuses

@login_required
def families(request):
    'Show families, or send to Buses landing page if no Buses'
    if not IntakeBuses.objects.exists():
        return redirect('intake buses')
    return HttpResponse("This is what you see on the family view and when there are buses.")
    # if request.method =='POST':
    #     form = FamilyForm(request.POST)
    #     if form.is_valid():
    #         return HttpResponseRedirect('home')
    # else:
    #     form = FamilyForm()
    # return render(request, 'intake/family-add.html', {'form': form})

class FamilyAddPageView(LoginRequiredMixin, TemplateView):
    template_name = "intake/family-add.html"

    def get_context_data(self, **kwargs):
        context = super(FamilyAddPageView, self).get_context_data(**kwargs)
        context['form'] = FamilyForm()
        context['model'] = 'Family'
        messages.info(self.request, "hello fam")
        return context
