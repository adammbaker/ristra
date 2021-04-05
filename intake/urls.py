from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import accounts, asylee, campaign, headofhousehold, intakebus
from intake.views import donate, location, medical, organization, reports, requestqueue, signup, sponsor, travelplan, users, views

urlpatterns = [
    # path('', central_dispatch.dispatch, name='dispatch'),
    path('', views.HomePageView.as_view(), name='home'),
    path('requestqueue', requestqueue.request_queue, name='request queue'),
    # path('token/<int:poc_id>/', tokens.token_generate, name='org token generate'),
    # path('organization', organization.OrganizationCreationView.as_view(), name='families'),
    path('signup/', accounts.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', signup.ActivateAccount.as_view(), name='activate'),
    path('cardtest', views.cardtest, name='card test'),

    path('organization/', include(([
        path('list/<user_id>/', organization.OrganizationListView.as_view(), name='list'),
        path('add/<user_id>', organization.OrganizationCreateView.as_view(), name='add'),
        path('<org_id>/detail', organization.OrganizationDetail.as_view(), name='detail'),
        # path('<org_id>/detail', organization.OrganizationDetailView.as_view(), name='detail'),
        path('<org_id>/overview', organization.OrganizationOverview.as_view(), name='overview'),
        path('<org_id>/edit', organization.OrganizationEditView.as_view(), name='edit'),
        path('<org_id>/update', organization.OrganizationUpdate.as_view(), name='update'),
        # path('', organization.OrganizationListView.as_view(), name='list'),
        # path('add/', organization.OrganizationCreationView.as_view(), name='add'),
        # path('<org_id>/', organization.OrganizationDetailView.as_view(), name='detail'),
        # path('campaigns/<org_id>/', campaign.CampaignListView.as_view(), name='campaigns'),
        path('approve/<int:queue_id>/', requestqueue.organization_approve, name='approve'),
        path('decline/<int:queue_id>/', requestqueue.organization_decline, name='decline'),
    ], 'intake'), namespace='organization')),

    path('location/', include(([
        # path('list/<org_id>', location.LocationList.as_view(), name='list'),
        path('add/<org_id>', location.LocationCreateView.as_view(), name='add'),
        # path('<loc_id>/detail', location.LocationDetailView.as_view(), name='detail'),
        path('<loc_id>/overview', location.LocationOverview.as_view(), name='overview'),
        path('<loc_id>/detail', location.LocationDetail.as_view(), name='detail'),
        path('<loc_id>/update', location.LocationUpdate.as_view(), name='update'),
        path('<loc_id>/delete', location.LocationDelete.as_view(), name='delete'),
        # path('<loc_id>/', location.LocationListView.as_view(), name='list'),
        # path('<loc_id>/', location.LocationDetailView.as_view(), name='detail'),
        # path('add/<org_id>/', location.LocationCreationView.as_view(), name='add'),
        # path('edit/<loc_id>/', location.LocationUpdateView.as_view(), name='edit'),
    ], 'intake'), namespace='location')),

    path('intakebus/', include(([
        path('list/<loc_id>', intakebus.IntakeBusListView.as_view(), name='list'),
        path('add/<loc_id>', intakebus.IntakeBusCreateView.as_view(), name='add'),
        # path('<ib_id>/detail', intakebus.IntakeBusDetailView.as_view(), name='detail'),
        path('<ib_id>/detail', intakebus.IntakeBusDetail.as_view(), name='detail'),
        path('<ib_id>/overview', intakebus.IntakeBusOverview.as_view(), name='overview'),
        path('<ib_id>/update', intakebus.IntakeBusUpdate.as_view(), name='update'),
        path('<ib_id>/delete', intakebus.IntakeBusDelete.as_view(), name='delete'),
        # path('<ib_id>/', intakebus.IntakeBusDetailView.as_view(), name='detail'),
        # path('add/<loc_id>/', intakebus.IntakeBusCreationView.as_view(), name='add'),
    ], 'intake'), namespace='intakebus')),

    # path('family/', include(([
    #     path('list/<ib_id>', family.FamilyListView.as_view(), name='list'),
    #     path('add/<ib_id>', family.FamilyCreateView.as_view(), name='add'),
    #     path('<fam_id>/detail', family.FamilyDetailView.as_view(), name='detail'),
    #     path('<fam_id>/edit', family.FamilyEditView.as_view(), name='edit'),
    #     # path('<fam_id>/', family.FamilyDetailView.as_view(), name='detail'),
    #     # path('add/<ib_id>/', family.FamilyCreationView.as_view(), name='add'),
    # ], 'intake'), namespace='family')),

    path('headofhousehold/', include(([
        path('list/<ib_id>', headofhousehold.HeadOfHouseholdListView.as_view(), name='list'),
        path('add/<ib_id>', headofhousehold.HeadOfHouseholdCreateView.as_view(), name='add'),
        # path('<hoh_id>/detail', headofhousehold.HeadOfHouseholdDetailView.as_view(), name='detail'),
        path('<hoh_id>/detail', headofhousehold.HeadOfHouseholdDetail.as_view(), name='detail'),
        path('<hoh_id>/overview', headofhousehold.HeadOfHouseholdOverview.as_view(), name='overview'),
        path('<hoh_id>/update', headofhousehold.HeadOfHouseholdUpdate.as_view(), name='update'),
        path('<hoh_id>/delete', headofhousehold.HeadOfHouseholdDelete.as_view(), name='delete'),
        path('<hoh_id>/itinerary', headofhousehold.ItineraryDetail.as_view(), name='itinerary'),
        path('followup/health/<hoh_id>', headofhousehold.HeadOfHouseholdHealthFollowUpTemplateView.as_view(), name='health follow up'),
        path('<hoh_id>/add/<need_id>', headofhousehold.AddNeedToHousehold, name='add need'),
        path('<hoh_id>/satisfy/<need_id>', headofhousehold.SatisfyNeedForHousehold, name='satisfy need'),
        # path('<hoh_id>/', headofhousehold.HeadOfHouseholdDetailView.as_view(), name='detail'),
        # path('add/<ib_id>/', headofhousehold.HeadOfHouseholdCreationView.as_view(), name='add'),
    ], 'intake'), namespace='headofhousehold')),

    path('asylee/', include(([
        path('list/<hoh_id>', asylee.AsyleeListView.as_view(), name='list'),
        path('add/<hoh_id>', asylee.AsyleeCreateView.as_view(), name='add'),
        # path('<asy_id>/detail', asylee.AsyleeDetailView.as_view(), name='detail'),
        path('<asy_id>/detail', asylee.AsyleeDetail.as_view(), name='detail'),
        path('<asy_id>/overview', asylee.AsyleeOverview.as_view(), name='overview'),
        path('<asy_id>/update', asylee.AsyleeUpdate.as_view(), name='update'),
        path('<asy_id>/delete', asylee.AsyleeDelete.as_view(), name='delete'),
        # path('followup/health /<asy_id>', asylee.AsyleeHealthFollowUpFormView.as_view(), name='health follow up'),
        path('followup/<asy_id>', asylee.AsyleeHealthFollowUpTemplateView.as_view(), name='health follow up'),
        # path('<asylee_id>/', asylee.AsyleeDetailView.as_view(), name='detail'),
        # path('add/<hoh_id>/', asylee.AsyleeCreationView.as_view(), name='add'),
    ], 'intake'), namespace='asylee')),

    path('sponsor/', include(([
        path('list/<hoh_id>', sponsor.SponsorListView.as_view(), name='list'),
        path('add/<hoh_id>', sponsor.SponsorCreateView.as_view(), name='add'),
        path('<spon_id>/detail', sponsor.SponsorDetailView.as_view(), name='detail'),
        path('<spon_id>/update', sponsor.SponsorUpdate.as_view(), name='update'),
        path('<spon_id>/delete', sponsor.SponsorDelete.as_view(), name='delete'),
        # path('<sponsor_id>/', sponsor.SponsorDetailView.as_view(), name='detail'),
        # path('add/<hoh_id>/', sponsor.SponsorCreationView.as_view(), name='add'),
    ], 'intake'), namespace='sponsor')),

    path('travelplan/', include(([
        path('list/<hoh_id>', travelplan.TravelPlanListView.as_view(), name='list'),
        path('add/<hoh_id>', travelplan.TravelPlanCreateView.as_view(), name='add'),
        path('<tp_id>/detail', travelplan.TravelPlanDetailView.as_view(), name='detail'),
        path('<tp_id>/update', travelplan.TravelPlanUpdate.as_view(), name='update'),
        path('<tp_id>/delete', travelplan.TravelPlanDelete.as_view(), name='delete'),
        path('followup/<tp_id>', travelplan.TravelModeFollowUpTemplateView.as_view(), name='travel follow up'),
        # path('<tp_id>/', travelplan.TravelPlanDetailView.as_view(), name='detail'),
        # path('add/<hoh_id>/', travelplan.TravelPlanCreationView.as_view(), name='add'),
    ], 'intake'), namespace='travelplan')),

    # path('medical/', include(([
    #     path('list/<asy_id>', medical.MedicalListView.as_view(), name='list'),
    #     path('add/<asy_id>', medical.MedicalCreateView.as_view(), name='add'),
    #     path('<med_id>/detail', medical.MedicalDetailView.as_view(), name='detail'),
    #     path('<med_id>/update', medical.MedicalUpdate.as_view(), name='update'),
    #     path('<med_id>/delete', medical.MedicalDelete.as_view(), name='delete'),
    #     # path('<med_id>/', medical.MedicalDetailView.as_view(), name='detail'),
    #     # path('add/<asylee_id>/', medical.MedicalCreationView.as_view(), name='add'),
    # ], 'intake'), namespace='medical')),

    path('campaign/', include(([
        path('list/<user_id>', campaign.CampaignListView.as_view(), name='list'),
        path('add/<user_id>', campaign.CampaignCreateView.as_view(), name='add'),
        path('<camp_id>/detail', campaign.CampaignDetailView.as_view(), name='detail'),
        # path('add/', campaign.CampaignCreationView.as_view(), name='add'),
        # path('<camp_id>/', campaign.CampaignDetailView.as_view(), name='detail'),
        path('affiliate/<camp_id>/', campaign.affiliate, name='affiliate'),
    ], 'intake'), namespace='campaign')),

    path('user/', include(([
    #     path('', point_of_contact.QuizListView.as_view(), name='quiz_list'),
        path('request_permission/', users.request_permission_to_create_organization, name='request permission'),
        path('approve/<int:queue_id>/', users.approve_organization_creation, name='approve'),
        path('decline/<int:queue_id>/', users.approve_organization_creation, name='decline'),
        path('affiliate/<org_id>/', users.affiliate_user_to_organization, name='affiliate'),
        path('update_profile/', accounts.ProfileFormView.as_view(), name='update profile'),
    #     path('taken/', point_of_contact.TakenQuizListView.as_view(), name='taken_quiz_list'),
    #     path('quiz/<int:pk>/', point_of_contact.take_quiz, name='take_quiz'),
    ], 'intake'), namespace='user')),

    path('report/', include(([
        path('ataglance', reports.AtAGlance.as_view(), name='at a glance'),
        path('households/active', reports.ActiveHouseholds.as_view(), name='active households'),
        path('asylees/active', reports.ActiveAsylees.as_view(), name='active asylees'),
        path('households/lacking_travel_plan', reports.HouseholdsLackingTravelPlan.as_view(), name='hohs lack tp'),
        path('households/lacking_sponsor', reports.HouseholdsLackingSponsor.as_view(), name='hohs lack spon'),
        path('asylees/lacking_a_number', reports.AsyleesLackingANumber.as_view(), name='asys lack anum'),
        path('households/arrived_yesterday', reports.HouseholdsArrivedYesterday.as_view(), name='hohs arr yday'),
        path('households/arrived_today', reports.HouseholdsArrivedToday.as_view(), name='hohs arr today'),
        path('households/leaving_tomorrow', reports.HouseholdsLeavingTomorrow.as_view(), name='hohs lvg tom'),
        path('households/leaving_today', reports.HouseholdsLeavingToday.as_view(), name='hohs lvg today'),
        path('asylees/search', reports.ReportSearch.as_view(), name='asylees search'),
        path('volunteers/search', reports.VolunteerSearch.as_view(), name='volunteers search'),
        path('households/lacking_departure_bags', reports.HouseholdsLackingDepartureBags.as_view(), name='hohs departurebags'),
        path('households/lacking_travel_food', reports.HouseholdsLackingTravelFood.as_view(), name='hohs travelfood'),
        # path('add/<hoh_id>', reports.TravelPlanCreateView.as_view(), name='add'),
        # path('<tp_id>/detail', reports.TravelPlanDetailView.as_view(), name='detail'),
        # path('<tp_id>/update', reports.TravelPlanUpdate.as_view(), name='update'),
        # path('<tp_id>/delete', reports.TravelPlanDelete.as_view(), name='delete'),
        # path('followup/<tp_id>', reports.TravelModeFollowUpTemplateView.as_view(), name='travel follow up'),
    ], 'intake'), namespace='report')),

    path('donate/', include(([
        path('', donate.DonateList.as_view(), name='overview'),
        path('add', donate.DonateCreate.as_view(), name='add'),
        path('delete/<pk>', donate.DonateDelete.as_view(), name='delete'),
        path('update/<pk>', donate.DonateUpdate.as_view(), name='update'),
    ], 'intake'), namespace='donate')),

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
