from rest_framework import serializers
from .models import Parameter
from .models import DataAyam, DataAyamHistory

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'timestamp', 'ammonia', 'temperature', 'humidity', 'score']
        
from rest_framework import serializers
from .models import DataAyam, DataAyamHistory

class DataAyamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAyam
        fields = ['id', 'timestamp', 'tanggal_mulai', 'jumlah_ayam_awal', 'tanggal_panen', 'jumlah_ayam', 'mortalitas', 'usia_ayam']
        
    def get_history(self, obj):
        # Ambil history terkait dengan instance ini
        histories = obj.history.all().order_by('-timestamp')
        return DataAyamHistorySerializer(histories, many=True).data
    
    def update(self, instance, validated_data):
        # Simpan data lama untuk history
        DataAyamHistory.objects.create(
            data_ayam=instance,
            jumlah_ayam_awal=instance.jumlah_ayam_awal,
            tanggal_mulai=instance.tanggal_mulai,
            tanggal_panen=instance.tanggal_panen,
            jumlah_ayam=instance.jumlah_ayam,
            mortalitas=instance.mortalitas,
            usia_ayam=instance.usia_ayam
        )
        
        # Update instance dengan data baru
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class DataAyamHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAyamHistory
        fields = ['id', 'data_ayam', 'jumlah_ayam_awal', 'tanggal_mulai', 'tanggal_panen', 'jumlah_ayam', 'mortalitas', 'usia_ayam', 'timestamp']
