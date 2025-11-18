from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    co2_ppm = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"T: {self.temperature} ºC, H: {self.humidity} %, CO2: {self.co2_ppm} ppm"
