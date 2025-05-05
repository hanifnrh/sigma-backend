from rest_framework import serializers
from api.models import Alat


class AlatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Alat
        fields = ['alat_id', 'battery_level', 'api_key']
        extra_kwargs = {
            'alat_id': {'validators': []} #Ini dimatikan untuk mencegah error
        }

    def validate_alat_id(self, value):

        if Alat.objects.filter(alat_id = value).exists():
            return value
        return value

    def create(self, validated_data):
        alat, _ = Alat.objects.update_or_create(
            alat_id = validated_data["alat_id"],
            defaults = {
                "battery_level": validated_data["battery_level"]
            }
        )
        return alat
