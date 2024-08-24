from django.contrib import admin
from .models import Doctor, Patient, Appointment, MedicalRecord
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.html import format_html
from django.shortcuts import render
from django.template.response import TemplateResponse




class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_full_name', 'specialty', 'phone_number']
    search_fields = ['user__username', 'first_name', 'last_name', 'specialty']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'

class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'gender']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_filter = ['gender']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'appointment_time', 'get_slot', 'status']
    list_filter = ['doctor', 'appointment_time', 'status']
    search_fields = ['doctor__first_name', 'doctor__last_name', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'appointment_time'
    actions = ['mark_consulted', 'mark_skipped']

    def get_slot(self, obj):
        return obj.patient.slot
    get_slot.short_description = 'Time Slot'

    def get_queryset(self, request):
        # Return all appointments without any filtering
        return super().get_queryset(request)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:appointment_id>/consulted/', self.admin_site.admin_view(self.consulted_action), name='appointment-consulted'),
            path('<int:appointment_id>/skip/', self.admin_site.admin_view(self.skip_action), name='appointment-skip'),
        ]
        return custom_urls + urls

    def consulted_action(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = 'completed'
        appointment.save()

        MedicalRecord.objects.create(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment=appointment,
            record_date=timezone.now().date()
        )

        self.message_user(request, "Appointment marked as consulted and medical record created.")
        return HttpResponseRedirect("../../")

    def skip_action(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = 'skipped'
        appointment.save()

        self.message_user(request, "Appointment marked as skipped.")
        return HttpResponseRedirect("../../")

    def mark_consulted(self, request, queryset):
        for appointment in queryset:
            self.consulted_action(request, appointment.id)
    mark_consulted.short_description = "Mark selected appointments as consulted"

    def mark_skipped(self, request, queryset):
        for appointment in queryset:
            self.skip_action(request, appointment.id)
    mark_skipped.short_description = "Mark selected appointments as skipped"

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor_name', 'appointment', 'styled_record_date', 'styled_appointment_status']
    list_filter = ['doctor', 'record_date', 'appointment__status']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    date_hierarchy = 'record_date'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('patient', 'doctor', 'appointment', 'record_date')
        return self.readonly_fields

    def patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    patient_name.short_description = 'Patient'

    def doctor_name(self, obj):
        return f"{obj.doctor.first_name} {obj.doctor.last_name}"
    doctor_name.short_description = 'Doctor'

    def styled_record_date(self, obj):
        return format_html('<span style="background-color: #blue; padding: 3px 7px; border-radius: 3px;">{}</span>', obj.record_date.strftime('%Y-%m-%d'))
    styled_record_date.short_description = 'Record Date'

    def styled_appointment_status(self, obj):
        if obj.appointment:
            status = obj.appointment.status
            color = {
                'scheduled': 'blue',
                'completed': 'green',
                'skipped': 'red'
            }.get(status, 'gray')
            return format_html('<span style="background-color: {}; color: white; padding: 3px 7px; border-radius: 3px;">{}</span>', color, status.capitalize())
        return 'N/A'
    styled_appointment_status.short_description = 'Status'

admin.site.register(MedicalRecord, MedicalRecordAdmin)