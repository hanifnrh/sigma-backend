from rest_framework import serializers
from .models import Parameter
from .models import DataAyam, DataAyamHistory

from rest_framework import serializers
from .models import Parameter
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role')

class ParameterSerializer(serializers.ModelSerializer):
    ammonia_status = serializers.SerializerMethodField()
    temperature_status = serializers.SerializerMethodField()
    humidity_status = serializers.SerializerMethodField()
    ammonia_color = serializers.SerializerMethodField()
    temperature_color = serializers.SerializerMethodField()
    humidity_color = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Parameter
        fields = [
            'id', 'timestamp', 'ammonia', 'temperature', 'humidity',
            'ammonia_status', 'temperature_status', 'humidity_status',
            'ammonia_color', 'temperature_color', 'humidity_color',
            'status', 'color', 'score'
        ]
        read_only_fields = ['id', 'timestamp', 'status', 'color', 'score']

    def get_ammonia_status(self, obj):
        if obj.ammonia > 30:
            return "Bahaya"
        elif obj.ammonia > 25:
            return "Buruk"
        elif obj.ammonia > 20:
            return "Baik"
        else:
            return "Sangat Baik"

    def get_temperature_status(self, obj):
        if obj.temperature < 18 or obj.temperature > 36:
            return "Bahaya"
        elif obj.temperature >= 18 and obj.temperature <= 23 or obj.temperature >= 35 and obj.temperature <= 36:
            return "Buruk"
        elif obj.temperature >= 24 and obj.temperature <= 25 or obj.temperature >= 33 and obj.temperature <= 34:
            return "Baik"
        else:
            return "Sangat Baik"

    def get_humidity_status(self, obj):
        if obj.humidity < 58 or obj.humidity > 72:
            return "Bahaya"
        elif obj.humidity >= 58 and obj.humidity <= 59 or obj.humidity >= 71 and obj.humidity <= 72:
            return "Buruk"
        elif obj.humidity >= 60 and obj.humidity <= 61 or obj.humidity >= 69 and obj.humidity <= 70:
            return "Baik"
        else:
            return "Sangat Baik"
        
    def get_ammonia_color(self, obj):
        return obj.get_ammonia_color()

    def get_temperature_color(self, obj):
        return obj.get_temperature_color()

    def get_humidity_color(self, obj):
        return obj.get_humidity_color()
    
    def get_color(self, obj):
        return obj.get_status_color()


    
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

#create alat serializer here





#create transkrip serializer here