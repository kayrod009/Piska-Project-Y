from django.db import models


class Patient(models.Model):
    username = models.CharField(max_length=300)
    password = models.IntegerField()
    email = models.EmailField(max_length=264)


class Clinic(models.Model):
    name = models.CharField(max_length=300)
    capacity = models.IntegerField()


class Staff(models.Model):
    username = models.CharField(max_length=300)
    password = models.IntegerField()
    email = models.EmailField(max_length=264)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)


class Doctors(models.Model):
    name = models.CharField(max_length=300)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    status = models.IntegerField()
