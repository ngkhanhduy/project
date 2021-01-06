from django.db import models

# Create your models here.

class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"from {self.location} to {self.destination}"

class place(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=20,decimal_places=15)
    long = models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return f"{self.name}"