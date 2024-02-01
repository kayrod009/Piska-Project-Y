from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    # Other URLs...
]