from django.shortcuts import render, redirect
from .models import Patient, Staff  # Make sure to import your models

def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('userType')
        email = request.POST.get('email')
        password = int(request.POST.get('password'))  # Convert password to int

        if user_type == 'بیمار':
            user = Patient.objects.filter(email=email, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['user_type'] = 'patient'
                return redirect('patient_dashboard')
            else:
                return render(request, 'Clinic/login.html', {'error': 'Patient not found'})

        elif user_type == 'منشی':
            user = Staff.objects.filter(email=email, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['user_type'] = 'staff'
                return redirect('staff_dashboard')
            else:
                return render(request, 'Clinic/login.html', {'error': 'Staff not found'})

    return render(request, 'Clinic/login.html')

def patient_dashboard(request):
    if 'user_id' in request.session and request.session['user_type'] == 'patient':
        return render(request, 'Clinic/patient_dashboard.html')
    else:
        return redirect('login')

def staff_dashboard(request):
    if 'user_id' in request.session and request.session['user_type'] == 'staff':
        return render(request, 'Clinic/staff_dashboard.html')
    else:
        return redirect('login')