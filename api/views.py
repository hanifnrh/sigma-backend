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
from .models import StartFarming
from .serializers import StartFarmingSerializer

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
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # Perform the deletion
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class StartFarmingListCreate(generics.ListCreateAPIView):
    queryset = StartFarming.objects.all()
    serializer_class = StartFarmingSerializer
    
class StartFarmingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StartFarming.objects.all()
    serializer_class = StartFarmingSerializer
    
@api_view(['PATCH'])
def update_jumlah_ayam(request, pk):
    try:
        # Ambil data ayam yang ada
        data_ayam = DataAyam.objects.get(pk=pk)

        # Simpan riwayat data ayam yang lama ke DataAyamHistory
        DataAyamHistory.objects.create(
            data_ayam=data_ayam,
            jumlah_ayam_awal=data_ayam.jumlah_ayam_awal,
            tanggal_panen=data_ayam.tanggal_panen,
            jumlah_ayam=data_ayam.jumlah_ayam,
            mortalitas=data_ayam.mortalitas,
            usia_ayam=data_ayam.usia_ayam,
        )

        # Update data ayam dengan data yang baru
        for key, value in request.data.items():
            setattr(data_ayam, key, value)
        data_ayam.save()

        # Kirimkan response setelah data diperbarui
        serializer = DataAyamSerializer(data_ayam)
        return Response(serializer.data)

    except DataAyam.DoesNotExist:
        return Response({'error': 'DataAyam not found'}, status=404)