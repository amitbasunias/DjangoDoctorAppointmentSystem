# Generated by Django 4.2.4 on 2023-08-29 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0004_customuser_approved_appointments'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='prescription_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='max_patient_appointments',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='customuser',
            name='vacation_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='vacation_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='vacation_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=100)),
                ('patient_email', models.EmailField(max_length=254)),
                ('patient_age', models.PositiveIntegerField()),
                ('patient_gender', models.CharField(max_length=10)),
                ('symptoms', models.TextField(blank=True, null=True)),
                ('recommended_tests', models.TextField(blank=True, null=True)),
                ('prescribed_medicine', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_created', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
