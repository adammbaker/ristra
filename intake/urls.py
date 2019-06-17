from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import views

urlpatterns = [
    # path('', central_dispatch.dispatch, name='dispatch'),
    path('', views.HomePageView.as_view(), name='home'),

    # path('poc/', include(([
    #     path('', point_of_contact.QuizListView.as_view(), name='quiz_list'),
    #     path('interests/', point_of_contact.StudentInterestsView.as_view(), name='student_interests'),
    #     path('taken/', point_of_contact.TakenQuizListView.as_view(), name='taken_quiz_list'),
    #     path('quiz/<int:pk>/', point_of_contact.take_quiz, name='take_quiz'),
    # ], 'classroom'), namespace='point_of_contact')),
    #
    # path('teachers/', include(([
    #     path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
    #     path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
    #     path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
    #     path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
    #     path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
    #     path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
    #     path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
    #     path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    # ], 'classroom'), namespace='teachers')),

    path('landing', views.landing_page, name='landing page'),
    path('staging', views.staging, name='staging ground'),
    path('organization/add', organizations.organization_add, name='organization add'),
    path('organization/<int:id>/', organizations.organization_detail, name='org detail'),
    # path('organization/<int:id>/affiliate', organizations.organization_affiliate, name='org affiliate'),
    path('organization/<int:id>/affiliate/<str:campaign>', organizations.organization_affiliate, name='org affiliate'),
    path('organization/<int:id>/admin', organizations.organization_detail_admin, name='org detail admin'),
    path('organization/<int:id>/edit', organizations.organization_detail_fill, name='org detail fill'),
    path('organization/<int:id>/publicize', organizations.organization_pubilicize, name='org publicize'),
    path('locations/', locations.locations, name='locations'),
    path('location/add/', locations.location_add, name='location add'),
    path('location/add/<int:id>', locations.location_add, name='location add to org'),
    path('intakebuses/', intakebuses.intake_buses, name='intake buses'),
    path('intakebuses/add/', intakebuses.IntakeBusAddPageView.as_view(), name='intake bus add'),
    path('family/', family.families, name='families'),
    path('family/add/', family.FamilyAddPageView.as_view(), name='family add'),
    # path('signup/', signup.signup, name='signup'),
    # path('index/', views.index, name='index'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('qr/', views.qr_code, name='qr'),
    path('user/', views.user_overview, name='user overview'),
    # re_path(r'^join/(?P<secret>\w+)/$', views.join_organization, name='join org'),
    # re_path(r'^organizations/join/(?P<secret>[\w-]+)/$', organizations.organization_join, name='org join'),
    # re_path(r'^organizations/(?P<id>\w+)/$', organizations.organization_overview, name='org overview'),
]
