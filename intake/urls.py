from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import family, intakebuses, locations, signup, views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('landing/', views.landing_page, name='landing page'),
    path('locations/', locations.locations, name='locations'),
    path('locations/add/', locations.LocationAddPageView.as_view(), name='location add'),
    path('intakebuses/', intakebuses.intake_buses, name='intake buses'),
    path('intakebuses/add/', intakebuses.IntakeBusAddPageView.as_view(), name='intake bus add'),
    path('family/', family.families, name='families'),
    path('family/add/', family.FamilyAddPageView.as_view(), name='family add'),
    path('signup/', signup.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', auth_views.LoginView.as_view(), name='login'),
]
