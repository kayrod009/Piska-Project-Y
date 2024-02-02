from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Patient, Staff, Clinic  # Make sure to import your models
from django.views.decorators.http import require_POST


def login_view(request):
    # Simply render and return the login.html template
    return render(request, 'Clinic/login.html')


@require_POST
def process_patient_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Consider using Django's password management

        # Create and save the new Patient instance
        patient = Patient(username=username, email=email, password=password)  # Adjust according to your model
        patient.save()

        # Redirect to a new URL, e.g., the login page, after successful signup
        return redirect('login')  # Replace 'login_url' with the actual name of your login view

    # If not a POST request, you might redirect to the signup form again or handle differently
    return redirect('patient_signup')  # Redirects to the page-rendering view if not a POST request


def patient_signup(request):
    # Simply render and return the patient_signup.html template
    return render(request, 'Clinic/patient_signup.html')


def process_staff_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Password is not hashed per your request
        clinic_id = request.POST.get('clinicId')  # Assuming you still want to capture the clinic ID

        # Create and save the new Staff member without checking for clinic existence
        staff_member = Staff(username=username, email=email, password=password, clinic_id=clinic_id)
        staff_member.save()

        # Redirect to a success page, login page, or wherever you want after signup
        return redirect('login')  # Adjust the redirect as needed
    else:
        # If not a POST request, just render the staff signup form
        return render(request, 'Clinic/staff_signup.html')


def staff_signup(request):
    # Render and return the staff_signup.html template
    return render(request, 'Clinic/staff_signup.html')