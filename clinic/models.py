from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='doctors'
    )
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=30)
    experience_years = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.age > 120:
            raise ValidationError({'age': 'Age must be realistic (0-120).'})


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments'
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Scheduled'
    )

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.appointment_date}"

    def clean(self):
        if self.appointment_date and self.appointment_date < timezone.now().date():
            raise ValidationError(
                {'appointment_date': 'Appointment date cannot be in the past.'}
            )


class Medicine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dosage_form = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name='prescription'
    )
    medicines = models.ManyToManyField(Medicine, related_name='prescriptions')
    diagnosis = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment}"
