from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Patient, Staff, Clinic, Appointment, Doctors  # Make sure to import your models
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import logout


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


def process_login(request):
    if request.method == 'POST':
        user_type = request.POST.get('userType')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = None
        if user_type == 'منشی':
            user = Staff.objects.filter(email=email, password=password).first()
            dashboard_url = 'staff_dashboard'  # URL name for staff dashboard
        elif user_type == 'بیمار':
            user = Patient.objects.filter(email=email, password=password).first()
            dashboard_url = 'patient_dashboard'  # URL name for patient dashboard

        if user is not None:
            request.session['user_id'] = user.id
            request.session['user_type'] = user_type
            return redirect(dashboard_url)
        else:
            messages.error(request, 'Login failed. Please check your credentials.')

    # If GET request or login failed, render the login page
    return render(request, 'Clinic/login.html')


def staff_dashboard_view(request):
    return render(request, 'Clinic/staff_dashboard.html')


def patient_dashboard_view(request):
    # Assume 'patient_id' is stored in the session or use request.user if authenticated
    patient_id = request.session.get('user_id')  # Or request.user.id for authenticated user

    # Fetch appointments
    in_action_appointments = Appointment.objects.filter(patient_id=patient_id, status=1)
    completed_appointments = Appointment.objects.filter(patient_id=patient_id, status=0)

    # Pass appointments to the template
    context = {
        'in_action_appointments': in_action_appointments,
        'completed_appointments': completed_appointments
    }
    return render(request, 'Clinic/patient_dashboard.html', context)

def logout_view(request):
    logout(request)
    # Redirect to a success page, such as the home page or the login page
    return redirect('login')  # Replace 'login' with the name of your login URL


def search_clinics_doctors(request):
    search_key = request.GET.get('searchKey', '')

    clinics = Clinic.objects.filter(name__icontains=search_key, capacity__gt=0)
    doctors = Doctors.objects.filter(name__icontains=search_key)

    # Include all clinics if a doctor is found, to allow clinic selection in the form
    if doctors:
        clinics = Clinic.objects.filter(capacity__gt=0)

    return render(request, 'Clinic/patient_dashboard.html', {
        'clinics': clinics,
        'doctors': doctors,
        'search_key': search_key,
        'search_results': True,
    })


def book_appointment(request):
    if request.method == 'POST':
        # Extract information from the POST request
        clinic_id = request.POST.get('clinic')
        doctor_id = request.POST.get('doctor')
        patient_id = request.session.get('user_id')  # Assuming you store patient ID in session

        # Fetch the clinic and doctor instances
        clinic = Clinic.objects.get(id=clinic_id)
        doctor = Doctors.objects.get(id=doctor_id)

        # Create an appointment
        Appointment.objects.create(patient_id=patient_id, doctor=doctor, clinic=clinic, status=1)

        # Decrease the clinic's capacity by 1 and save
        clinic.capacity -= 1
        clinic.save()

        # Redirect to a success page or back to the dashboard with a success message
        return redirect('patient_dashboard')  # Replace with your success URL

    # If not a POST request, redirect to the form page or show an error
    return redirect('patient_dashboard')  # Replace with your form URL or error handling

@require_POST  # Ensure that this view only handles POST requests
def cancel_appointment(request, appointment_id):
    # Ensure the staff member is authorized to cancel the appointment
    # This is important for security reasons
    appointment = Appointment.objects.get(id=appointment_id)
    # You might want to check that the appointment's clinic matches the staff's clinic
    # For simplicity, this check is omitted here
    appointment.delete()  # Delete the appointment
    # Redirect back to the staff dashboard after deletion
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))