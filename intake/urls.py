from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import asylee, campaign, family, intakebus, location, medical, organization, requestqueue, sponsor, travelplan, tokens, views

urlpatterns = [
    # path('', central_dispatch.dispatch, name='dispatch'),
    path('', views.HomePageView.as_view(), name='home'),
    path('', views.HomePageView.as_view(), name='families'),
    path('requestqueue', requestqueue.request_queue, name='request queue'),
    # path('token/<int:poc_id>/', tokens.token_generate, name='org token generate'),
    # path('organization', organization.OrganizationCreationView.as_view(), name='families'),

    path('organization/', include(([
        path('add/', organization.OrganizationCreationView.as_view(), name='add'),
        path('<org_id>/', organization.OrganizationDetailView.as_view(), name='detail'),
        path('campaigns/<org_id>/', campaign.CampaignListView.as_view(), name='campaigns'),
        path('approve/<int:queue_id>/', requestqueue.organization_approve, name='approve'),
        path('decline/<int:queue_id>/', requestqueue.organization_decline, name='decline'),
    ], 'intake'), namespace='organization')),

    path('location/', include(([
        path('<loc_id>/', location.LocationDetailView.as_view(), name='detail'),
        path('add/<org_id>/', location.LocationCreationView.as_view(), name='add'),
        path('edit/<loc_id>/', location.LocationUpdateView.as_view(), name='edit'),
    ], 'intake'), namespace='location')),

    path('intakebus/', include(([
        path('<ib_id>/', intakebus.IntakeBusDetailView.as_view(), name='detail'),
        path('add/<loc_id>/', intakebus.IntakeBusCreationView.as_view(), name='add'),
    ], 'intake'), namespace='intakebus')),

    path('family/', include(([
        path('<fam_id>/', family.FamilyDetailView.as_view(), name='detail'),
        path('add/<ib_id>/', family.FamilyCreationView.as_view(), name='add'),
    ], 'intake'), namespace='family')),

    path('asylee/', include(([
        path('<asylee_id>/', asylee.AsyleeDetailView.as_view(), name='detail'),
        path('add/<fam_id>/', asylee.AsyleeCreationView.as_view(), name='add'),
    ], 'intake'), namespace='asylee')),

    path('medical/', include(([
        path('<med_id>/', medical.MedicalDetailView.as_view(), name='detail'),
        path('add/<asylee_id>/', medical.MedicalCreationView.as_view(), name='add'),
    ], 'intake'), namespace='medical')),

    path('sponsor/', include(([
        path('<sponsor_id>/', sponsor.SponsorDetailView.as_view(), name='detail'),
        path('add/<fam_id>/', sponsor.SponsorCreationView.as_view(), name='add'),
    ], 'intake'), namespace='sponsor')),

    path('travelplan/', include(([
        path('<tp_id>/', travelplan.TravelPlanDetailView.as_view(), name='detail'),
        path('add/<fam_id>/', travelplan.TravelPlanCreationView.as_view(), name='add'),
    ], 'intake'), namespace='travelplan')),

    path('campaign/', include(([
        path('add/', campaign.CampaignCreationView.as_view(), name='add'),
        path('<camp_id>/', campaign.CampaignDetailView.as_view(), name='detail'),
        path('affiliate/<camp_id>/', campaign.affiliate, name='affiliate'),
    ], 'intake'), namespace='campaign')),

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
    # path('organization/add', organizations.organization_add, name='organization add'),
    # path('organization/<int:id>/', organizations.organization_detail, name='org detail'),
    # path('organization/<int:id>/affiliate', organizations.organization_affiliate, name='org affiliate'),
    # path('organization/<int:id>/affiliate/<str:campaign>', organizations.organization_affiliate, name='org affiliate'),
    # path('organization/<int:id>/admin', organizations.organization_detail_admin, name='org detail admin'),
    # path('organization/<int:id>/edit', organizations.organization_detail_fill, name='org detail fill'),
    # path('organization/<int:id>/publicize', organizations.organization_pubilicize, name='org publicize'),
    # path('locations/', locations.locations, name='locations'),
    # path('location/add/', locations.location_add, name='location add'),
    # path('location/add/<int:id>', locations.location_add, name='location add to org'),
    # path('intakebuses/', intakebuses.intake_buses, name='intake buses'),
    # path('intakebuses/add/', intakebuses.IntakeBusAddPageView.as_view(), name='intake bus add'),
    # path('family/', family.families, name='families'),
    # path('family/add/', family.FamilyAddPageView.as_view(), name='family add'),
    # path('signup/', signup.signup, name='signup'),
    # path('index/', views.index, name='index'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('qr/', views.qr_code, name='qr'),
    path('user/', views.user_detail, name='user detail'),
    # re_path(r'^join/(?P<secret>\w+)/$', views.join_organization, name='join org'),
    # re_path(r'^organizations/join/(?P<secret>[\w-]+)/$', organizations.organization_join, name='org join'),
    # re_path(r'^organizations/(?P<id>\w+)/$', organizations.organization_overview, name='org overview'),
]
