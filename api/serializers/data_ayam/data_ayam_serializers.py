
from api.models import DataAyam, DataAyamHistory
from rest_framework import serializers


class DataAyamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAyam
        fields = ['id', 'timestamp', 'tanggal_mulai', 'jumlah_ayam_awal', 'tanggal_panen', 'jumlah_ayam', 'mortalitas', 'usia_ayam']




    def update(self, instance, validated_data):
        #lacak nilai sebelumnya sebelum pembaruan
        original_data = {
            "jumlah_ayam" : instance.jumlah_ayam,
            "tanggal_panen": instance.tanggal_panen,
            "usia_ayam": instance.usia_ayam
        }

        #apply pembaruan ke instance (jangan disimpan dulu)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)


        #Simpan data lama untuk history
        if any(original_data[field] != getattr(instance, field) for field in original_data):
            DataAyamHistory.objects.create(
                data_ayam=instance,
                jumlah_ayam_awal=instance.jumlah_ayam_awal,
                tanggal_mulai=instance.tanggal_mulai,
                tanggal_panen=instance.tanggal_panen,
                jumlah_ayam=instance.jumlah_ayam,
                mortalitas=instance.mortalitas,
                usia_ayam=instance.usia_ayam
            )
        #DataAyamHistory.objects.create(data_ayam=instance,)
        
        
        #simpan instance terbaru
        instance.save()
        return instance