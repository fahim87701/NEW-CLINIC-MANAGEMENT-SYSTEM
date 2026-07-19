from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, DoctorViewSet, PatientViewSet,
    AppointmentViewSet, MedicineViewSet, PrescriptionViewSet,
)

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('doctors', DoctorViewSet)
router.register('patients', PatientViewSet)
router.register('appointments', AppointmentViewSet)
router.register('medicines', MedicineViewSet)
router.register('prescriptions', PrescriptionViewSet)

urlpatterns = router.urls
