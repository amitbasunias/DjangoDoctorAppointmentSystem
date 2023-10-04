from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    specialist = models.CharField(max_length=50, blank=True)  # Specialist field for all users

    is_available = models.BooleanField(default=True)
    max_patient_appointments = models.PositiveIntegerField(default=5)
    vacation_mode = models.BooleanField(default=False)
    vacation_start_date = models.DateField(null=True, blank=True)
    vacation_end_date = models.DateField(null=True, blank=True)
    custom_availabilities = models.JSONField(default=dict, blank=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.user_type == 'doctor':
            self.specialist = models.CharField(max_length=50)  # Add Specialist field for doctors
        super(CustomUser, self).save(*args, **kwargs)
    approved_appointments = models.ManyToManyField('Appointment', related_name='approved_doctors', blank=True)

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    appointment_datetime = models.DateTimeField()
    prescription_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment from {self.patient} to {self.doctor} on {self.appointment_datetime}"

class Prescription(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prescriptions_created')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prescriptions_received')
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(max_length=10)

    symptoms = models.TextField(blank=True, null=True)
    recommended_tests = models.TextField(blank=True, null=True)
    prescribed_medicine = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription from {self.doctor} to {self.patient}"
