from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from intake.views import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),

    # path('organization/', include(([
    #     path('', students.QuizListView.as_view(), name='quiz_list'),
    #     path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
    #     path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
    #     path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    # ], 'classroom'), namespace='organization')),
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
]
