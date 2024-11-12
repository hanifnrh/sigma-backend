from rest_framework import serializers
from .models import Parameter
from .models import DataAyam
from .models import StartFarming

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'timestamp', 'ammonia', 'temperature', 'humidity']
        
class DataAyamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAyam
        fields = ['id', 'timestamp', 'tanggal_mulai', 'jumlah_ayam_awal', 'tanggal_panen', 'jumlah_ayam', 'mortalitas', 'usia_ayam']
        
class StartFarmingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartFarming
        fields = ['id', 'jumlah_ayam', 'target_tanggal', 'tanggal_mulai']
