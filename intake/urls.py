from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import signup, views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', signup.signup, name='signup'),
    path('index', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('login', auth_views.LoginView.as_view(), name='login'),
]
