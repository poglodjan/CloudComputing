from django.contrib import admin
from django.urls import path, include
from app.views import (
    StudentDetailView, TeacherListView, ParentListView,
    WritingDataCreateView, ShapesDataCreateView, EmotionsDataCreateView,
    TeacherCreateView, ParentCreateView, StudentListCreateView,
    WritingDatasetListView, ShapesDatasetListView, EmotionsDatasetListView,
    AutismSurveyListView, TeacherSurveyListView,
    AutismSurveyCreateView, TeacherSurveyCreateView, PredictEmotionsView, get_parent_email_by_student,
    PredictShapesView, PredictQuestionnaire1View, PredictQuestionnaire2View,
    PredictEnsembleView, GetTeacherIDView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #obsluga podaplikacji artykułów - psychosphere
    path(
    "api/psychosphere/",
    include("psychosphere.urls"),
    ),
    # GET users
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('parents/', ParentListView.as_view(), name='parent_list'),
    #path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('parent-email/<int:student_id>/', get_parent_email_by_student, name='parent-email-by-student'),
    path("api/teacher-id/", GetTeacherIDView.as_view(), name="get-teacher-id"),

    # POST endpoints (create)
    path('api/teachers/', TeacherCreateView.as_view(), name='teacher_create'),
    path('api/parents/', ParentCreateView.as_view(), name='parent_create'),
    path('api/writings/', WritingDataCreateView.as_view(), name='writing_data_create'),
    path('api/shapes/', ShapesDataCreateView.as_view(), name='shapes_data_create'),
    path('api/emotions/', EmotionsDataCreateView.as_view(), name='emotions_data_create'),
    path('api/autism_survey/', AutismSurveyCreateView.as_view(), name='emotions_data_create'),
    path('api/teacher_survey/', TeacherSurveyCreateView.as_view(), name='teacher_survey_create'),

    # GET & POST students
    path('students/', StudentListCreateView.as_view(), name='student_list'),
    path('students/<int:student_id>/', StudentDetailView.as_view(), name='student-detail'),

    # GET games and quests data (list)
    path('fact/writing_dataset/', WritingDatasetListView.as_view(), name='writing_dataset_list'),
    path('fact/shapes_dataset/', ShapesDatasetListView.as_view(), name='shapes_dataset_list'),
    path('fact/emotions_dataset/', EmotionsDatasetListView.as_view(), name='emotions_dataset_list'),
    path('fact/autism_survey/', AutismSurveyListView.as_view(), name='autism_survey_list'),
    path('fact/teacher_survey/', TeacherSurveyListView.as_view(), name='teacher_survey_list'),

    #MODEL
    path('predict_emotions/<int:student_id>/', PredictEmotionsView.as_view(), name='predict_emotions'),
    path('predict_shapes/<int:student_id>/', PredictShapesView.as_view(), name='predict_shapes'),
    path('predict_questionnaire_autism/<int:student_id>/', PredictQuestionnaire1View.as_view(), name='predict_questionnaire1'),
    path('predict_questionnaire_adhd/<int:student_id>/', PredictQuestionnaire2View.as_view(), name='predict_questionnaire2'),
    # ENSEMBLE
    path('predict_ensemble/<int:student_id>/', PredictEnsembleView.as_view(), name='predict_ensemble'),
]
    
