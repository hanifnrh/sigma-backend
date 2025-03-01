from rest_framework import serializers

from api.models import Parameter

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