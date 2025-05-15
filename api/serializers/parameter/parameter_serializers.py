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
            'status', 'color', 'floor', 'score'
        ]
        read_only_fields = ['id', 'timestamp', 'status', 'color', 'score']

    def get_ammonia_status(self, obj):
        
        return obj.get_ammonia_status()

    def get_temperature_status(self, obj):
        
        return obj.get_temperature_status()

    def get_humidity_status(self, obj):
        
        return obj.get_humidity_status()
        
    def get_ammonia_color(self, obj):
        return obj.get_ammonia_color()

    def get_temperature_color(self, obj):
        return obj.get_temperature_color()

    def get_humidity_color(self, obj):
        return obj.get_humidity_color()
    
    def get_color(self, obj):
        return obj.get_status_color()