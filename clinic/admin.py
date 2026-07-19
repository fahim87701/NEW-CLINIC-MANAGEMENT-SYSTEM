from django.contrib import admin
from .models import Department, Doctor, Patient, Appointment, Medicine, Prescription


class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [DoctorInline]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'department', 'experience_years', 'is_available')
    list_filter = ('department', 'is_available', 'specialization')
    search_fields = ('name', 'specialization', 'email')
    ordering = ('name',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'phone')
    list_filter = ('gender',)
    search_fields = ('name', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'doctor')
    search_fields = ('patient__name', 'doctor__name')
    ordering = ('appointment_date',)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage_form', 'price')
    search_fields = ('name',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'diagnosis', 'created_at')
    filter_horizontal = ('medicines',)
    readonly_fields = ('created_at',)
