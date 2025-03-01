from api.models import DataAyamHistory
from rest_framework import serializers

#data ayam history serializer
class DataAyamHistorySerializer(serializers.ModelSerializer):
    data_ayam_details = serializers.SerializerMethodField()
    class Meta:
        model = DataAyamHistory
        #fields = ['id', 'data_ayam', 'jumlah_ayam_awal', 'tanggal_mulai', 'tanggal_panen', 'jumlah_ayam', 'mortalitas', 'usia_ayam', 'timestamp']
        fields = ['id', 'data_ayam_id', 'data_ayam_details', 'timestamp']

    def get_data_ayam_details(self, obj):
        return {
            "jumlah_ayam": obj.jumlah_ayam,
            "mortalitas": obj.mortalitas,
            "usia_ayam": obj.usia_ayam,
            "tanggal_mulai": obj.tanggal_mulai,
            "jumlah_ayam_awal": obj.jumlah_ayam_awal,
            "tanggal_panen": obj.tanggal_panen,
        }
