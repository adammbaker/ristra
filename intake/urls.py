from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import family, intakebuses, locations, organizations, signup, views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('landing/', views.landing_page, name='landing page'),
    path('organizations/', organizations.organizations, name='organizations'),
    # path('organizations/add/', organizations.OrganizationAddPageView.as_view(), name='organization add'),
    path('locations/', locations.locations, name='locations'),
    path('locations/add/', locations.LocationAddPageView.as_view(), name='location add'),
    path('intakebuses/', intakebuses.intake_buses, name='intake buses'),
    path('intakebuses/add/', intakebuses.IntakeBusAddPageView.as_view(), name='intake bus add'),
    path('family/', family.families, name='families'),
    path('family/add/', family.FamilyAddPageView.as_view(), name='family add'),
    path('signup/', signup.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('qr/', views.qr_code, name='qr'),
    path('user/', views.user_overview, name='user overview'),
    re_path(r'^join/(?P<secret>\w+)/$', views.join_organization, name='join org'),
    # re_path(r'^organizations/join/(?P<secret>[\w-]+)/$', organizations.organization_join, name='org join'),
    path('organizations/join/', organizations.organization_join, name='org join'),
    # re_path(r'^organizations/(?P<id>\w+)/$', organizations.organization_overview, name='org overview'),
    path('organizations/<int:id>/', organizations.organization_overview, name='org overview'),
]
