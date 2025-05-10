from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'recruitment'

urlpatterns = [
    path('', views.home, name='home'),
    path('interviews/', views.interview_list, name='interview_list'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/new/', views.candidate_create, name='candidate_create'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('candidates/<int:pk>/edit/', views.candidate_edit, name='candidate_edit'),
    path('candidates/<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    # Staff position management URLs
    path('positions/', views.position_list, name='position_list'),
    path('positions/create/', views.position_create, name='position_create'),
    path('positions/<int:pk>/', views.position_detail, name='position_detail'),
    path('positions/<int:pk>/edit/', views.position_edit, name='position_edit'),
    path('positions/<int:pk>/toggle/', views.position_toggle, name='position_toggle'),
    
    # Public position URLs
    path('careers/positions/', views.public_position_list, name='public_position_list'),
    path('careers/positions/<int:pk>/', views.public_position_detail, name='public_position_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='recruitment/login.html'), name='login'),
    # Thay thế LogoutView bằng custom logout view
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.candidate_profile, name='candidate_profile'),
    
    # Staff URLs
    path('staff/login/', views.staff_login, name='staff_login'),
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('interviewer/dashboard/', views.interviewer_dashboard, name='interviewer_dashboard'),
    
    # Calendar URLs
    path('calendar/', views.interview_calendar, name='interview_calendar'),
    path('calendar/events/', views.get_interview_events, name='get_interview_events'),
    path('calendar/schedule/', views.schedule_interview, name='schedule_interview'),
    path('interview/confirm/<int:interview_id>/', views.confirm_interview, name='confirm_interview'),
    
    path('applications/', views.application_management, name='application_management'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
    path('applications/export/', views.export_applications, name='export_applications'),
]