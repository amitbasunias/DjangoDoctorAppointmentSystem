from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register_moderator/', views.register_moderator, name='register_moderator'),
    path('logout/', views.logout_user, name='logout'),
    path('request-appointment/', views.request_appointment, name='request_appointment'),
    path('manage-appointments/', views.doctor_manage_appointments, name='doctor_manage_appointments'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/create_prescription/', views.create_prescription, name='create_prescription'),
    path('doctor/set_availability/', views.set_availability, name='set_availability'),
    path('doctor/set_vacation_mode/', views.set_vacation_mode, name='set_vacation_mode'),

    # ... other URL patterns ...
]
