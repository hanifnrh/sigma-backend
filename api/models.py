from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

#User
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('staf', 'Staf'),
        ('pemilik', 'Pemilik')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staf')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Tambahkan related_name untuk menghindari konflik
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Tambahkan related_name untuk menghindari konflik
        blank=True,
    )

#model untuk alat
class Alat(models.Model):
    STATUS_CHOICES = [
        (0, 'Aktif'),
        (1, 'Nonaktif')
    ]
    alat_id = models.CharField(max_length = 255, unique = True)
    battery_level = models.FloatField()
    status = models.IntegerField(default = 0, choices=STATUS_CHOICES)

#model untuk parameter
class Parameter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ammonia = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, default="Error")

    def calculate_score(self):
        THRESHOLDS = {
            "ammonia": {"optimal": 20, "good": 25, "bad": 30},
            "temperature": {
                "veryGood": [26, 32],
                "good": [[24, 25], [33, 34]],
                "bad": [[18, 23], [35, 36]],
            },
            "humidity": {
                "veryGood": [62, 68],
                "good": [[60, 61], [69, 70]],
                "bad": [[58, 59], [71, 72]],
            },
        }

        def calculate_individual_score(value, thresholds, param_type):
            if param_type == "ammonia":
                if value <= thresholds["optimal"]:
                    return 100
                elif value <= thresholds["good"]:
                    return 75
                elif value <= thresholds["bad"]:
                    return 50
                else:
                    return 25
            elif param_type == "temperature":
                if thresholds["veryGood"][0] <= value <= thresholds["veryGood"][1]:
                    return 100
                elif any(r[0] <= value <= r[1] for r in thresholds["good"]):
                    return 75
                elif any(r[0] <= value <= r[1] for r in thresholds["bad"]):
                    return 50
                else:
                    return 25
            elif param_type == "humidity":
                if thresholds["veryGood"][0] <= value <= thresholds["veryGood"][1]:
                    return 100
                elif any(r[0] <= value <= r[1] for r in thresholds["good"]):
                    return 75
                elif any(r[0] <= value <= r[1] for r in thresholds["bad"]):
                    return 50
                else:
                    return 25
            return 50  # Fallback score

        ammonia_score = calculate_individual_score(self.ammonia, THRESHOLDS["ammonia"], "ammonia")
        temperature_score = calculate_individual_score(self.temperature, THRESHOLDS["temperature"], "temperature")
        humidity_score = calculate_individual_score(self.humidity, THRESHOLDS["humidity"], "humidity")

        return (ammonia_score + temperature_score + humidity_score) / 3

    def calculate_status(self):
        status_values = []

        if self.ammonia > 30:
            status_values.append("Bahaya")
        elif self.ammonia > 25:
            status_values.append("Buruk")
        elif self.ammonia > 20:
            status_values.append("Baik")
        else:
            status_values.append("Sangat Baik")

        if self.temperature < 18 or self.temperature > 36:
            status_values.append("Bahaya")
        elif self.temperature >= 18 and self.temperature <= 23 or self.temperature >= 35 and self.temperature <= 36:
            status_values.append("Buruk")
        elif self.temperature >= 24 and self.temperature <= 25 or self.temperature >= 33 and self.temperature <= 34:
            status_values.append("Baik")
        else:
            status_values.append("Sangat Baik")

        if self.humidity < 58 or self.humidity > 72:
            status_values.append("Bahaya")
        elif self.humidity >= 58 and self.humidity <= 59 or self.humidity >= 71 and self.humidity <= 72:
            status_values.append("Buruk")
        elif self.humidity >= 60 and self.humidity <= 61 or self.humidity >= 69 and self.humidity <= 70:
            status_values.append("Baik")
        else:
            status_values.append("Sangat Baik")

        if "Bahaya" in status_values:
            return "Bahaya"

        score = self.calculate_score()
        if score >= 90:
            return "Sangat Baik"
        elif score >= 70:
            return "Baik"
        elif score >= 50:
            return "Buruk"
        else:
            return "Bahaya"

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        self.status = self.calculate_status() or "Error"
        super().save(*args, **kwargs)

    def get_status_color(self):
        if self.status == "Sangat Baik":
            return "text-green-500"
        elif self.status == "Baik":
            return "text-blue-500"
        elif self.status == "Buruk":
            return "text-yellow-500"
        else:
            return "text-red-500"

    def get_ammonia_color(self):
        if self.ammonia > 30:
            return "text-red-500"
        elif self.ammonia > 25:
            return "text-yellow-500"
        elif self.ammonia > 20:
            return "text-blue-500"
        else:
            return "text-green-500"

    def get_temperature_color(self):
        if self.temperature < 18 or self.temperature > 36:
            return "text-red-500"
        elif self.temperature >= 18 and self.temperature <= 23 or self.temperature >= 35 and self.temperature <= 36:
            return "text-yellow-500"
        elif self.temperature >= 24 and self.temperature <= 25 or self.temperature >= 33 and self.temperature <= 34:
            return "text-blue-500"
        else:
            return "text-green-500"

    def get_humidity_color(self):
        if self.humidity < 58 or self.humidity > 72:
            return "text-red-500"
        elif self.humidity >= 58 and self.humidity <= 59 or self.humidity >= 71 and self.humidity <= 72:
            return "text-yellow-500"
        elif self.humidity >= 60 and self.humidity <= 61 or self.humidity >= 69 and self.humidity <= 70:
            return "text-blue-500"
        else:
            return "text-green-500"

class DataAyam(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    jumlah_ayam_awal = models.IntegerField()
    tanggal_mulai = models.DateField()
    tanggal_panen = models.DateField()
    jumlah_ayam = models.IntegerField()
    mortalitas = models.FloatField()
    usia_ayam = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.timestamp} - Jumlah Ayam Awal: {self.jumlah_ayam_awal}, , Tanggal Mulai: {self.tanggal_mulai} Tanggal Panen: {self.tanggal_panen}, Jumlah Ayam: {self.jumlah_ayam}, Mortalitas: {self.mortalitas}, Usia Ayam: {self.usia_ayam}"

class DataAyamHistory(models.Model):
    data_ayam = models.ForeignKey(DataAyam, on_delete=models.CASCADE, related_name="history")
    jumlah_ayam_awal = models.IntegerField()
    tanggal_mulai = models.DateField()
    tanggal_panen = models.DateField()
    jumlah_ayam = models.IntegerField()
    mortalitas = models.FloatField()
    usia_ayam = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add = True)  

    def __str__(self):
        return f"History {self.data_ayam_id} - Jumlah Ayam: {self.jumlah_ayam}, Tanggal Panen: {self.tanggal_panen}"
    
#create alat model here




#create transkrip model here 