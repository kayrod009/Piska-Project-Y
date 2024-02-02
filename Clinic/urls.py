from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),  # Ensure this matches
    path('process_patient_signup/', views.process_patient_signup, name='process_patient_signup'),
    path('staff_signup/', views.staff_signup, name='staff_signup'),
    path('process_staff_signup/', views.process_staff_signup, name='process_staff_signup'),
    # Other URLs...
]