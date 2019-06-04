from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.views.generic.base import TemplateView

from intake.encryption import Encryption
from intake.forms.organizations import OrganizationForm
from intake.models import Organizations, Volunteers

from socket import gethostname, gethostbyname

@login_required
def organizations(request):
    'Show organizations, or send to organization add if no Organizations'
    if not Organizations.objects.exists():
        if request.method =='POST':
            form = OrganizationForm(request.POST)
            if form.is_valid():
                org = form.save(commit=False)
                org.save()
                print('Saving organization:', Organizations.objects.last())
                print(request.user.username, 'is being added to org')
                return redirect('families') #TK should redirect to bus add upon location add or possibly a landing page asking the user what they want to do
        else:
            form = OrganizationForm()
        return render(request, 'intake/organization-add.html', {'form': form})

    return HttpResponse("This is what you see on the organizations view and when there are organizations.")

@login_required
def organization_join(request):
    'Shows the page required to join an organization'
    secret = request.GET.get('org_id')
    print('CODE:', secret)
    for org in Organizations.objects.all():
        dec = Encryption(org.name)
        # print('DEC',dec.decode(secret))
        if dec.decode(secret) == str(org.id):
            print('Adding %(user)s to %(org)s' % {
                'user': request.user.username,
                'org': org.name
            })
            vol = get_object_or_404(Volunteers, user__username=request.user.username)
            vol.organizations.add(org)
            vol.save()
    return HttpResponse('%(secret)s found' % {'secret': secret})

@login_required
def organization_overview(request, id):
    'Shows the information overview page for the requested organization'
    print('ID',id,type(id))
    org = get_object_or_404(Organizations, id=id)
    org.obscure_code()
    print('CODE:',org.code)
    template = loader.get_template('intake/organization-overview.html')
    context = {
        'org': org,
        'qr_url': 'http://%(hn)s:8000/organizations/join/?org_id=%(enc)s' % {
            'hn': gethostbyname(gethostname()),
            'enc': org.code,
        }
    }
    return HttpResponse(template.render(context, request))

# class OrganizationAddPageView(LoginRequiredMixin, TemplateView):
#     template_name = "intake/organization-add.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(OrganizationAddPageView, self).get_context_data(**kwargs)
#         context['form'] = OrganizationForm()
#         context['model'] = 'Organization'
#         messages.info(self.request, "hello org")
#         return context
