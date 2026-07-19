from rest_framework import viewsets
from .models import Department, Doctor, Patient, Appointment, Medicine, Prescription
from .serializers import (
    DepartmentSerializer, DoctorSerializer, PatientSerializer,
    AppointmentSerializer, MedicineSerializer, PrescriptionSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name']
    ordering_fields = ['name']


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filterset_fields = ['department', 'is_available', 'specialization']
    search_fields = ['name', 'specialization', 'email']
    ordering_fields = ['name', 'experience_years']


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filterset_fields = ['gender']
    search_fields = ['name', 'phone']
    ordering_fields = ['name', 'age']


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['status', 'doctor', 'patient', 'appointment_date']
    search_fields = ['patient__name', 'doctor__name', 'reason']
    ordering_fields = ['appointment_date', 'appointment_time']


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filterset_fields = ['dosage_form']
    search_fields = ['name']
    ordering_fields = ['name', 'price']


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    filterset_fields = ['appointment']
    search_fields = ['diagnosis']
    ordering_fields = ['created_at']
