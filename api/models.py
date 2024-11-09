from django.db import models

class Parameter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ammonia = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - Ammonia: {self.ammonia}, Temp: {self.temperature}, Humidity: {self.humidity}"
    
class DataAyam(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    jumlah_ayam_awal = models.IntegerField()
    tanggal_panen = models.DateField()
    jumlah_ayam = models.IntegerField()
    mortalitas = models.FloatField()
    usia_ayam = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.timestamp} - Jumlah Ayam Awal: {self.jumlah_ayam_awal}, Tanggal Panen: {self.tanggal_panen}, Jumlah Ayam: {self.jumlah_ayam}, Mortalitas: {self.mortalitas}, Usia Ayam: {self.usia_ayam}"

class DataAyamHistory(models.Model):
    data_ayam = models.ForeignKey(DataAyam, on_delete=models.CASCADE, related_name="history")
    jumlah_ayam_awal = models.IntegerField()
    tanggal_panen = models.DateField()
    jumlah_ayam = models.IntegerField()
    mortalitas = models.FloatField()
    usia_ayam = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Tanggal dan waktu saat perubahan tercatat

    def __str__(self):
        return f"History {self.data_ayam.id} - Jumlah Ayam: {self.jumlah_ayam}, Tanggal Panen: {self.tanggal_panen}"

class StartFarming(models.Model):
    jumlah_ayam = models.IntegerField()
    target_tanggal = models.DateField()
    tanggal_mulai = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Start Farming {self.id} - {self.jumlah_ayam} ayam"