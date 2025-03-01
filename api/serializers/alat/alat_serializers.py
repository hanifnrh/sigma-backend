from rest_framework import serializers
from api.models import Alat


class AlatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Alat
        fields = ['alat_id', 'battery_level', 'status']

class AlatTokenSerializer(serializers.Serializer):
    
    alat_id = serializers.CharField()
   
    #periksa apakah alat id muncul di basis data
    def validate_alat_id(self, value):
        try: 
            alat = Alat.objects.get(alat_id = value)
        except Alat.DoesNotExist:
            return serializers.ValidationError("ID alat tidak valid")
