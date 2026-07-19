# Clinic Appointment System

A backend REST API for managing a clinic's departments, doctors, patients, appointments, medicines, and prescriptions — built with Django and Django REST Framework.

## Problem Statement

Clinics need a simple way to track which doctor belongs to which department, which patient has booked an appointment with which doctor, and what prescription (with which medicines) resulted from that appointment. This project models that workflow as a relational database and exposes it through a full set of REST APIs.

## Features

- Full CRUD REST APIs for Departments, Doctors, Patients, Appointments, Medicines, and Prescriptions
- Relational design: ForeignKey (Doctor→Department, Appointment→Patient/Doctor), OneToOne (Prescription→Appointment), ManyToMany (Prescription↔Medicine)
- Model-level validation (`clean()`), field-level validation, and serializer/cross-field validation (e.g. no double-booking a doctor)
- Filtering, searching, and ordering on every list endpoint
- Page-number pagination on every list endpoint
- Customized Django Admin panel (list_display, search_fields, list_filter, inlines, filter_horizontal, readonly_fields)
- Read access is public; create/update/delete requires authentication (`IsAuthenticatedOrReadOnly`)

## Technologies Used

- Python 3
- Django 6
- Django REST Framework
- django-filter
- SQLite

## Project Structure

```
clinic_appointment_system/
├── clinic_project/        # project settings, root urls
├── clinic/                 # app: models, serializers, views, urls, admin
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt
```

## Database Migration Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Running the Project

```bash
python manage.py runserver
```

- Admin panel: http://127.0.0.1:8000/admin/
- API root: http://127.0.0.1:8000/api/

## API Endpoint List

| Resource | Endpoint |
|---|---|
| Departments | `/api/departments/` |
| Doctors | `/api/doctors/` |
| Patients | `/api/patients/` |
| Appointments | `/api/appointments/` |
| Medicines | `/api/medicines/` |
| Prescriptions | `/api/prescriptions/` |

Each endpoint supports: `GET` (list), `POST` (create), `GET /id/` (retrieve), `PUT /id/` (update), `PATCH /id/` (partial update), `DELETE /id/`.

### Filtering, Searching, Ordering examples

```
GET /api/doctors/?department=1
GET /api/doctors/?search=cardio
GET /api/doctors/?ordering=-experience_years

GET /api/appointments/?status=Scheduled
GET /api/appointments/?search=Rahim
GET /api/appointments/?ordering=appointment_date
```

## Sample API Requests and Responses

**Create a department**
```
POST /api/departments/
{
  "name": "Cardiology",
  "description": "Heart and cardiovascular care"
}
```

**Create a doctor**
```
POST /api/doctors/
{
  "name": "Dr. Anika Rahman",
  "specialization": "Cardiologist",
  "department": 1,
  "phone": "01711111111",
  "email": "anika@clinic.com",
  "license_number": "LIC-2024-001",
  "experience_years": 8,
  "is_available": true
}
```

**Book an appointment**
```
POST /api/appointments/
{
  "patient": 1,
  "doctor": 1,
  "appointment_date": "2026-08-01",
  "appointment_time": "10:30:00",
  "reason": "Chest pain checkup"
}
```

**Validation error example (double-booking)**
```json
{
  "non_field_errors": ["This doctor already has an appointment at that date and time."]
}
```

**Paginated list response**
```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/doctors/?page=2",
  "previous": null,
  "results": [ { "id": 1, "name": "Dr. Anika Rahman", "...": "..." } ]
}
```

## API Testing

All endpoints were tested using the DRF Browsable API and Postman, covering Create, List, Retrieve, Update, Partial Update, and Delete for every model.
