
from .forms import UserRegistrationForm, ModeratorRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Appointment, Prescription
from .forms import PrescriptionForm, AvailabilityForm, VacationModeForm, CustomAvailabilityForm



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        specialist = request.POST.get('specialist')
        if user_type == 'doctor':
            user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                              user_type=user_type, specialist=specialist, password=password)
        else:
            user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                                  user_type=user_type,  password=password)
        # Log the user in
        login(request, user)
        return redirect('dashboard')  # Redirect to the appropriate page after registration
    return render(request, 'register.html')
def dashboard(request):

    return render(request, 'userdashboard.html')


def register_moderator(request):
    if request.method == 'POST':
        form = ModeratorRegistrationForm(request.POST)
        form.doctor = request.user  # Set the doctor attribute on the form instance
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect back to the doctor's dashboard
    else:
        form = ModeratorRegistrationForm()
    return render(request, 'userdashboard.html', {'moderator_form': form})




def request_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        appointment_datetime = request.POST.get('appointment_datetime')

        doctor = CustomUser.objects.get(id=doctor_id)

        appointment = Appointment.objects.create(patient=request.user, doctor=doctor, appointment_datetime=appointment_datetime)
        return redirect('dashboard')  # Redirect to the appropriate page

    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'request_appointment.html', {'doctors': doctors})

def doctor_manage_appointments(request):
    if request.user.user_type != 'doctor':
        return redirect('home')  # Redirect non-doctors

    appointments = Appointment.objects.filter(doctor=request.user, status='pending')

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')

        appointment = Appointment.objects.get(id=appointment_id)
        if action == 'approve':
            appointment.status = 'approved'
            request.user.approved_appointments.add(appointment)
        elif action == 'deny':
            appointment.status = 'denied'
        appointment.save()

    return render(request, 'doctor_manage_appointments.html', {'appointments': appointments})

def logout_user(request):
    logout(request)
    return redirect('login')

def patient_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'patient':
        approved_appointments = request.user.appointments.filter(status='approved')
        return render(request, 'patient_dashboard.html', {'approved_appointments': approved_appointments})
    return redirect('login')  # Redirect unauthorized users to the login page


def doctor_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        doctor = request.user
        appointments = Appointment.objects.filter(doctor=doctor)

        prescription_form = PrescriptionForm(request.POST or None)
        availability_form = AvailabilityForm(request.POST or None)
        vacation_mode_form = VacationModeForm(request.POST or None)

        if request.method == 'POST':
            if 'create_prescription' in request.POST:
                if prescription_form.is_valid():
                    # Process and save prescription form data
                    prescription_form.save(doctor, doctor)
                    return redirect('doctor_dashboard')

            elif 'set_availability' in request.POST:
                if availability_form.is_valid():
                    # Process and save availability form data
                    availability_form.save(doctor)
                    return redirect('doctor_dashboard')
            elif 'set_custom_availability' in request.POST:
                if CustomAvailabilityForm.is_valid():
                    date = CustomAvailabilityForm.cleaned_data['date']
                    start_time = CustomAvailabilityForm.cleaned_data['start_time']
                    end_time = CustomAvailabilityForm.cleaned_data['end_time']
                    custom_availability = {
                        'start_time': start_time,
                        'end_time': end_time
                    }
                    if date in doctor.custom_availabilities:
                        doctor.custom_availabilities[date].update(custom_availability)
                    else:
                        doctor.custom_availabilities[date] = custom_availability
                    doctor.save()
                    return redirect('doctor_dashboard')

            elif 'set_vacation_mode' in request.POST:
                if vacation_mode_form.is_valid():
                    # Process and save vacation mode form data
                    vacation_mode_form.save(doctor)
                    return redirect('doctor_dashboard')

        context = {
            'doctor': doctor,
            'appointments': appointments,
            'prescription_form': prescription_form,
            'availability_form': availability_form,
            'custom_availability_form': CustomAvailabilityForm(request.POST or None),
            'vacation_mode_form': vacation_mode_form
        }
        return render(request, 'doctor_dashboard.html', context)
    else:
        return redirect('login')


def create_prescription(request):
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        if request.method == 'POST':
            # Process prescription form data and save to database
            # Redirect back to the dashboard
            return redirect('doctor_dashboard')
    else:
        return redirect('login')

def set_availability(request):
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        if request.method == 'POST':
            # Process availability form data and save to database
            # Redirect back to the dashboard
            return redirect('doctor_dashboard')
    else:
        return redirect('login')

def set_vacation_mode(request):
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        if request.method == 'POST':
            # Process vacation mode form data and save to database
            # Redirect back to the dashboard
            return redirect('doctor_dashboard')
    else:
        return redirect('login')