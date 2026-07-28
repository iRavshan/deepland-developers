from django.urls import path
from apps.courses import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guide/', views.learning_guide, name='learning_guide'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/lesson/<int:lesson_order>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<slug:course_slug>/lesson/<int:lesson_order>/toggle-complete/', views.toggle_lesson_complete, name='toggle_lesson_complete'),
    path('courses/<slug:course_slug>/lesson/<int:lesson_order>/toggle-feedback/', views.toggle_lesson_feedback, name='toggle_lesson_feedback'),
]
