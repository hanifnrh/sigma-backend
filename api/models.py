from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import secrets
#Model untuk user
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('staf', 'Staf'),
        ('pemilik', 'Pemilik'),
        ('tamu', 'Tamu'),
    ]
    PROFILE_PICTURE_CHOICES = [
        (1, "PP1"),
        (2, "PP2"),
        (3, "PP3"),
        (4, "PP4"),
        (5, "PP5"),
    ]
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tamu')
    profile_picture = models.IntegerField(choices=PROFILE_PICTURE_CHOICES, default = 1)
    first_name = None #orang indonesia tidak mempunyai first name dan last name
    last_name = None
    full_name = models.CharField(max_length = 30, null = True, verbose_name="Nama lengkap")
    is_approved = models.BooleanField(default = False, verbose_name="Sudah di approve pemilik?")
    
    def __str__(self):
        return f"{self.username} - {self.role} - {self.email}"

#model untuk alat
class Alat(models.Model):
    alat_id = models.CharField(max_length = 255, unique = True)
    api_key = models.CharField(max_length=64, unique=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.api_key or self.api_key is None:
            self.api_key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alat_id}"

#model untuk parameter
class Parameter(models.Model):
    FLOOR_CHOICES = [
        (1, "Lantai 1"),
        (2, "Lantai 2"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    ammonia = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    floor = models.IntegerField(choices=FLOOR_CHOICES, default = 1)
    score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, default="Error")

    def calculate_score(self): #Hitung skor ammonia dan kelembapan
        THRESHOLDS = {
            "ammonia": {"optimal": 20, "good": 25, "bad": 30},
            "temperature": {
                "veryGood": [26, 32],
                "good": [[24, 25], [33, 34]],
                "bad": [[18, 23], [35, 36]],
            },
            "humidity": {
                "veryGood": [60, 70],
                "good": [[50, 59], [71, 80]],
                "bad": [[0, 49], [81, 100]],
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

    def calculate_status(self): #Cek status secara umum
        status_values = [
            self.get_ammonia_status(),
            self.get_humidity_status(),
            self.get_temperature_status()
        ]

        if "Bahaya" in status_values: #Jika salah satu status bahaya langsung kembalikan bahaya
            return "Bahaya"

        score = self.calculate_score() #lakukan kalkulasi score jika tidak ada status bahaya dari status_values
        if score >= 90:
            return "Sangat Baik"
        elif score >= 70:
            return "Baik"
        elif score >= 50:
            return "Buruk"
        else:
            return "Bahaya"

    def get_ammonia_status(self):
            if self.ammonia > 30:
                return "Bahaya"
            elif self.ammonia > 25:
                return "Buruk"
            elif self.ammonia > 20:
                return "Baik"
            else:
                return "Sangat Baik"

    def get_temperature_status(self):
            if self.temperature < 18 or self.temperature > 36:
                return "Bahaya"
            elif self.temperature >= 18 and self.temperature <= 23 or self.temperature >= 35 and self.temperature <= 36:
                return "Buruk"
            elif self.temperature >= 24 and self.temperature <= 25 or self.temperature >= 33 and self.temperature <= 34:
                return "Baik"
            else:
                return "Sangat Baik"

    def get_humidity_status(self):
            if self.humidity < 45 or self.humidity > 85:
                return "Bahaya"
            elif self.humidity >= 45 and self.humidity <= 49 or self.humidity >= 81 and self.humidity <= 85:
                return "Buruk"
            elif self.humidity >= 50 and self.humidity < 59 or self.humidity > 70 and self.humidity <= 80 :
                return "Baik"
            elif self.humidity >= 60 and self.humidity <= 70:
                return "Sangat Baik"





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
        if self.humidity < 45 or self.humidity > 85:
            return "text-red-500"
        elif self.temperature >= 18 and self.temperature <= 23 or self.temperature >= 35 and self.temperature <= 36:
            return "text-yellow-500"
        elif self.temperature >= 24 and self.temperature <= 25 or self.temperature >= 33 and self.temperature <= 34:
            return "text-blue-500"
        else:
            return "text-green-500"

    def get_humidity_color(self):
        if self.humidity < 45  or self.humidity > 85:
            return "text-red-500"
        elif self.humidity >= 45 and self.humidity <= 49 or self.humidity >= 81 and self.humidity <= 85:
            return "text-yellow-500"
        elif self.humidity >= 50 and self.humidity < 59 or self.humidity > 70 and self.humidity <= 80 :
            return "text-blue-500"
        elif self.humidity >= 60 and self.humidity <= 70:
            return "text-green-500"
        
        
    def __str__(self):
        return f"Stempel Waktu {self.timestamp} - Skor : {self.calculate_score()} - Status : {self.calculate_status()}"
    

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
        return f"History {self.data_ayam_id} - Stempel Waktu {self.timestamp} - Jumlah Ayam: {self.jumlah_ayam}, Tanggal Panen: {self.tanggal_panen}"
    
#create alat model here




#create transkrip model here 