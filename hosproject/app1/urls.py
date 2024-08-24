from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('doctor/', views.doctor, name='doctor'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/create/', views.patient_form_view, name='appointment'),
    path('patients/', views.patient_details, name='patient_details'),

    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/create/', views.patient_form_view, name='appointment'),
    path('make-appointment/<int:doctor_id>/', views.make_appointment, name='make_appointment'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    
    path('consulted/<int:appointment_id>/', views.consulted_action, name='consulted_action'),
    path('skip/<int:appointment_id>/', views.skip_action, name='skip_action'),
    

    path('upload_description/<int:appointment_id>/', views.upload_description, name='upload_description'),


    path('make-appointment/<int:doctor_id>/', views.make_appointment, name='make_appointment'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('add_description/<int:appointment_id>/', views.add_description, name='add_description'),

]
