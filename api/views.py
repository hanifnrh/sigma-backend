from rest_framework import generics
from .models import Parameter
from .serializers import ParameterSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from .models import DataAyam
from .serializers import DataAyamSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DataAyam, DataAyamHistory
from .serializers import DataAyamSerializer
from rest_framework import status
from .serializers import DataAyamHistorySerializer

# List and Create Parameter
class ParameterListCreate(generics.ListCreateAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer

# Retrieve, Update, and Delete Parameter
class ParameterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    
# List and Create Parameter
class DataAyamListCreate(generics.ListCreateAPIView):
    queryset = DataAyam.objects.all()
    serializer_class = DataAyamSerializer

# Retrieve, Update, and Delete Parameter
class DataAyamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataAyam.objects.all()
    serializer_class = DataAyamSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        original_data = {
            "jumlah_ayam": instance.jumlah_ayam,
            "mortalitas": instance.mortalitas,
            "usia_ayam": instance.usia_ayam,
        }

        # Update instance with validated data
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Simpan riwayat jika field tertentu berubah
        updated_data = serializer.validated_data
        if any(
            original_data[key] != updated_data.get(key, original_data[key])
            for key in ["jumlah_ayam", "mortalitas", "usia_ayam"]
        ):
            DataAyamHistory.objects.create(
                data_ayam=instance,
                jumlah_ayam_awal=instance.jumlah_ayam_awal,
                tanggal_mulai=instance.tanggal_mulai,
                tanggal_panen=instance.tanggal_panen,
                jumlah_ayam=updated_data.get("jumlah_ayam", instance.jumlah_ayam),
                mortalitas=updated_data.get("mortalitas", instance.mortalitas),
                usia_ayam=updated_data.get("usia_ayam", instance.usia_ayam),
            )

        # Simpan perubahan
        self.perform_update(serializer)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def get_data_ayam_history(request, pk):
    try:
        data_ayam = DataAyam.objects.get(pk=pk)
        history = data_ayam.history.all().order_by('-timestamp')
        serializer = DataAyamHistorySerializer(history, many=True)
        return Response(serializer.data)
    except DataAyam.DoesNotExist:
        return Response({"error": "DataAyam not found"}, status=404)