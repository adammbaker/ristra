from django.urls import include, path, re_path

from intake.views import signup, views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', signup.signup, name='signup'),
]
