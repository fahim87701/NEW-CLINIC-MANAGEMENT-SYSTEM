from datetime import date
from rest_framework import serializers
from .models import Department, Doctor, Patient, Appointment, Medicine, Prescription


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']


class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    # sensitive field: only accepted on write, never sent back in the response
    license_number = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'department', 'department_name',
            'phone', 'email', 'license_number', 'experience_years', 'is_available',
        ]

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years cannot be negative.")
        return value


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'phone', 'email', 'address']

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    # nested read-only representations for a friendlier GET response
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'patient_detail', 'doctor_detail',
            'appointment_date', 'appointment_time', 'reason', 'status',
        ]

    def validate_appointment_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    def validate(self, data):
        # cross-field / business-rule validation: no double-booking a doctor
        doctor = data.get('doctor', getattr(self.instance, 'doctor', None))
        appt_date = data.get('appointment_date', getattr(self.instance, 'appointment_date', None))
        appt_time = data.get('appointment_time', getattr(self.instance, 'appointment_time', None))

        qs = Appointment.objects.filter(
            doctor=doctor, appointment_date=appt_date, appointment_time=appt_time
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This doctor already has an appointment at that date and time."]}
            )
        return data


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'dosage_form', 'price']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value


class PrescriptionSerializer(serializers.ModelSerializer):
    medicines_detail = MedicineSerializer(source='medicines', many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'appointment', 'medicines', 'medicines_detail',
            'diagnosis', 'notes', 'created_at',
        ]
        read_only_fields = ['created_at']

    def validate_appointment(self, value):
        # prevent duplicate prescriptions on the same appointment (OneToOne rule)
        if self.instance is None and Prescription.objects.filter(appointment=value).exists():
            raise serializers.ValidationError("This appointment already has a prescription.")
        if value.status == 'Cancelled':
            raise serializers.ValidationError("Cannot write a prescription for a cancelled appointment.")
        return value

    def validate_medicines(self, value):
        if not value:
            raise serializers.ValidationError("A prescription must include at least one medicine.")
        return value
