from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),  # Ensure this matches
    path('process_patient_signup/', views.process_patient_signup, name='process_patient_signup'),
    path('staff_signup/', views.staff_signup, name='staff_signup'),
    path('process_staff_signup/', views.process_staff_signup, name='process_staff_signup'),
    path('process_login/', views.process_login, name='process_login'),
    path('staff_dashboard/', views.staff_dashboard_view, name='staff_dashboard'),
    path('patient_dashboard/', views.patient_dashboard_view, name='patient_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_clinics_doctors, name='search_clinics_doctors'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('increase_clinic_capacity/', views.increase_clinic_capacity, name='increase_clinic_capacity'),
    # Other URLs...
]