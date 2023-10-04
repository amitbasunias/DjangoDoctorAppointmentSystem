from django import forms
from .models import Prescription, CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password', 'user_type')


class ModeratorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user_type = 'moderator'
        instance.doctor = self.doctor  # Associate the moderator with the doctor
        if commit:
            instance.save()
        return instance



class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['symptoms', 'recommended_tests', 'prescribed_medicine']

    def save(self, doctor, patient):
        instance = super().save(commit=False)
        instance.doctor = doctor
        instance.patient = patient
        instance.patient_name = patient.get_full_name()
        instance.patient_email = patient.email
        instance.patient_age = patient.age  # Assume CustomUser model has an age field
        instance.patient_gender = patient.gender  # Assume CustomUser model has a gender field
        instance.save()

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['is_available', 'max_patient_appointments']

    def save(self, doctor):
        doctor.is_available = self.cleaned_data['is_available']
        doctor.max_patient_appointments = self.cleaned_data['max_patient_appointments']
        doctor.save()


class CustomAvailabilityForm(forms.Form):
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(label='Start Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(label='End Time', widget=forms.TimeInput(attrs={'type': 'time'}))
class VacationModeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['vacation_mode', 'vacation_start_date', 'vacation_end_date']

    def save(self, doctor):
        doctor.vacation_mode = self.cleaned_data['vacation_mode']
        doctor.vacation_start_date = self.cleaned_data['vacation_start_date']
        doctor.vacation_end_date = self.cleaned_data['vacation_end_date']
        doctor.save()
