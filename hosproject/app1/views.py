import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from.models import UserProfile
from django.contrib.auth import login,authenticate,logout
from .forms import CustomLoginForm
from django.contrib import messages
from .models import Doctor
from .forms import PatientForm
from .models import MedicalRecord, Doctor, Patient, Appointment
from django.utils import timezone
from datetime import datetime
from django.db.models import Subquery, Max



def index(request):
    return render(request,'app1/index.html')


def about(request):
    return render(request,'app1/about.html')


def testimonial(request):
    return render(request,'app1/testimonial.html')


def contact(request):
    return render(request,'app1/contact.html')



def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save()
            
            UserProfile.objects.create(
                user=user,   
            )
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app1/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username  
                if hasattr(user, 'doctor'):
                    return redirect('doctor_dashboard')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'app1/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')  



def patient_form_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()

            appointment_date = form.cleaned_data.get('appointment_date')
            slot = form.cleaned_data.get('slot')
            doctor = form.cleaned_data.get('doctor')

            if doctor and appointment_date and slot:
                appointment_time = datetime.datetime.combine(
                    appointment_date, 
                    datetime.datetime.strptime(slot.split('-')[0], '%I').time()
                )
                appointment = Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    appointment_time=appointment_time
                )

                MedicalRecord.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment=appointment,
                    record_date=appointment_date
                )

            messages.success(request, 'Appointment successfully created!')
            return redirect('appointment')
    else:
        form = PatientForm()

    return render(request, 'app1/appointment.html', {'form': form})




def doctor(request):
    data_value = Doctor.objects.all().order_by('-id')
    for data in data_value:
        if hasattr(data, 'description'):
            data.first_sentence = data.description.split('.')[0] + '.' if '.' in data.description else data.description
        else:
            data.first_sentence = ''  
    return render(request, 'app1/doctor.html', {'datas': data_value})





@login_required
def patient_details(request):
    appointments = Appointment.objects.filter(patient__user=request.user).select_related('patient')
    return render(request, 'app1/patients.html', {'appointments': appointments})

@login_required
def doctor_appointments(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.is_doctor:
        return redirect('index')
    
    doctor = user_profile.doctor
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient')
    return render(request, 'app1/doctor_appointments.html', {'appointments': appointments})
    
    
    
@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(
        doctor=request.user.doctor
    ).select_related('patient').order_by('appointment_time')
    return render(request, 'app1/doctor_dashboard.html', {'appointments': appointments})

@login_required
def make_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    show_all_doctors = request.GET.get('show_all', False)

    if show_all_doctors:
        appointments = Appointment.objects.filter(patient__user=request.user).select_related('patient', 'doctor').order_by('-appointment_time')
        latest_appointments = Appointment.objects.filter(
            id__in=Subquery(
                Appointment.objects.filter(patient__user=request.user)
                .values('patient')
                .annotate(latest_id=Max('id'))
                .values('latest_id')
            )
        ).select_related('patient', 'doctor').order_by('-appointment_time')
    else:
        appointments = Appointment.objects.filter(patient__user=request.user, doctor=doctor).select_related('patient', 'doctor').order_by('-appointment_time')
        latest_appointments = Appointment.objects.filter(
            id__in=Subquery(
                Appointment.objects.filter(patient__user=request.user, doctor=doctor)
                .values('patient')
                .annotate(latest_id=Max('id'))
                .values('latest_id')
            )
        ).select_related('patient', 'doctor').order_by('-appointment_time')

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            form = PatientForm(request.POST)  # Create a new form instance without the patient instance
        else:
            form = PatientForm(request.POST)

        if form.is_valid():
            if patient_id:
                # If it's an existing patient, create a new appointment without updating patient info
                appointment_date = form.cleaned_data.get('appointment_date')
                slot = form.cleaned_data.get('slot')

                if appointment_date and slot:
                    appointment_time = datetime.combine(
                        appointment_date, 
                        datetime.strptime(slot.split('-')[0], '%I').time()
                    )
                    appointment = Appointment.objects.create(
                        doctor=doctor,
                        patient=patient,
                        appointment_time=appointment_time
                    )

                    MedicalRecord.objects.create(
                        patient=patient,
                        doctor=doctor,
                        appointment=appointment,
                        record_date=appointment_date
                    )
            else:
                # If it's a new patient, save the new patient info and create an appointment
                patient = form.save(commit=False)
                patient.user = request.user
                patient.save()

                appointment_date = form.cleaned_data.get('appointment_date')
                slot = form.cleaned_data.get('slot')

                if appointment_date and slot:
                    appointment_time = datetime.combine(
                        appointment_date, 
                        datetime.strptime(slot.split('-')[0], '%I').time()
                    )
                    appointment = Appointment.objects.create(
                        doctor=doctor,
                        patient=patient,
                        appointment_time=appointment_time
                    )

                    MedicalRecord.objects.create(
                        patient=patient,
                        doctor=doctor,
                        appointment=appointment,
                        record_date=appointment_date
                    )
            
            return redirect('patient_detail', patient_id=patient.id)
    else:
        patient_id = request.GET.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            form = PatientForm(initial={
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'date_of_birth': patient.date_of_birth,
                'address': patient.address,
                'phone_number': patient.phone_number,
                'gender': patient.gender,
            })
        else:
            form = PatientForm()

    return render(request, 'app1/make_appointment.html', {
        'form': form,
        'doctor': doctor,
        'appointments': appointments,
        'latest_appointments': latest_appointments,
        'show_all_doctors': show_all_doctors,
    })



@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_time')
    
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'app1/patient_detail.html', context)












@login_required
def consulted_action(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    
    # Try to get an existing medical record for this appointment
    medical_record, created = MedicalRecord.objects.get_or_create(
        appointment=appointment,
        defaults={
            'patient': appointment.patient,
            'doctor': appointment.doctor,
            'record_date': timezone.now().date()
        }
    )
    
    if not created:
        # If the record already existed, you might want to update it
        medical_record.record_date = timezone.now().date()
        medical_record.save()
    
    # Optionally, mark the appointment as completed
    appointment.status = 'completed'  # Assuming you have a status field
    appointment.save()
    
    return redirect('doctor_dashboard')



@login_required
def skip_action(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    
    # Mark the appointment as skipped
    appointment.status = 'skipped'
    appointment.save()
    
    messages.success(request, "Appointment marked as skipped.")
    return redirect('doctor_dashboard')



@login_required
def upload_description(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    
    if request.method == 'POST':
        if 'description_file' in request.FILES:
            appointment.description_file = request.FILES['description_file']
            appointment.save()
            messages.success(request, 'Description file uploaded successfully.')
        else:
            messages.error(request, 'No file was uploaded.')
    
    return redirect('doctor_dashboard')


@login_required
def add_description(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user.doctor != appointment.doctor:
        return redirect('patient_detail', patient_id=appointment.patient.id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        description_file = request.FILES.get('description_file')
        
        if description:
            appointment.description = description
        
        if description_file:
            appointment.description_file = description_file
        
        appointment.save()
    
    return redirect('patient_detail', patient_id=appointment.patient.id)