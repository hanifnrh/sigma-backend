from django.core.cache import cache
from django.utils.timezone import now, timedelta
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import Parameter, DataAyam, DataAyamHistory, CustomUser, Alat

from .serializers.data_ayam_history.data_ayam_history_serializers import DataAyamHistorySerializer
from .serializers.data_ayam.data_ayam_serializers import DataAyamSerializer
from .serializers.user.user_serializers import UserSerializer
from .serializers.parameter.parameter_serializers import ParameterSerializer
from .serializers.alat.alat_serializers import AlatSerializer
from .permissions import IsAlatRole
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user' : UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)
    

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully!',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user




# List and Create Parameter
class ParameterListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParameterSerializer

    def get_queryset(self):
        queryset = Parameter.objects.all()
        floor = self.kwargs.get("floor")
        time_range = self.request.query_params.get("time_range", None)

        if floor:
            queryset = queryset.filter(floor=floor)
        
        if time_range:
            #unit waktu (m = menit, h = jam, d = hari, mo = bulan)
            try:
                if time_range.endswith("mo") : #bulan
                    value = int(time_range[:-2])
                    time_threshold = now() - timedelta(days = value * 30)
                else:
                    unit = time_range[-1]
                    value = int(time_range[:-1])

                    if unit == 'm': #menit
                        time_threshold = now() - timedelta(minutes = value)
                    elif unit == 'h': #jam
                        time_threshold = now() - timedelta(hours = value)
                    elif unit == 'd' : #hari
                        time_threshold = now() - timedelta(days = value)
            
                    else:
                        raise ValueError("Satuan waktu tidak valid")
                
                queryset = queryset.filter(timestamp__gte=time_threshold)
                    
            except (ValueError, TypeError):
                raise ValidationError ({"error": "format time_range tidak valid"})
                
        return queryset
    
    def perform_create(self, serializer):
        #memastikan nilai floor diambil dari url
        serializer.save(floor=self.kwargs.get("floor"))

# Bulk or delete all
class ParameterListDelete(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        param_ids = request.data.get("ids", None)

        if param_ids :
            deleted_count = Parameter.objects.filter(id__in=param_ids).count()
            Parameter.objects.filter(id__in=param_ids).delete()
            return Response({"message" : f"Berhasil menghapus {deleted_count} parameter"}, status = 200)
        
        #delete all if no specific ids provded
        deleted_count = Parameter.objects.count()
        Parameter.objects.all().delete()

        return Response({"message": f"Berhasil menghapus semua {deleted_count} parameter"}, status = 200)

# Retrieve, Update, and Delete specific Parameter
class ParameterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    
# List and Create DataAyam
class DataAyamListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataAyam.objects.all()
    serializer_class = DataAyamSerializer

# Bulk or delete all DataAyam
class DataAyamDelete(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        param_ids = request.data.get("ids", None)

        if param_ids :
            deleted_count = DataAyam.objects.filter(id__in=param_ids).count()
            DataAyam.objects.filter(id__in=param_ids).delete()
            return Response({"message" : f"Berhasil menghapus {deleted_count} data ayam"}, status = 200)
        
        #delete all if no specific ids provded
        deleted_count = DataAyam.objects.all().count()
        DataAyam.objects.all().delete()

        return Response({"message": f"Berhasil menghapus semua {deleted_count} data ayam"}, status = 200)

# Retrieve, Update, and Delete specific DataAyam
class DataAyamDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataAyam.objects.all()
    serializer_class = DataAyamSerializer

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial=True)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status = 400)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": " entry data ayam berhasil di hapus"}, status=204)

#List or create all
class DataAyamHistoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataAyamHistory.objects.all()
    serializer_class = DataAyamHistorySerializer

    def get_queryset(self):
        queryset = DataAyamHistory.objects.all()
        time_range = self.request.query_params.get("time_range", None)

        if time_range:
            #unit waktu (m = menit, h = jam, d = hari, mo = bulan)
            try:
                if time_range.endswith("mo") : #bulan
                    value = int(time_range[:-2])
                    time_threshold = now() - timedelta(days = value * 30)
                else:
                    unit = time_range[-1]
                    value = int(time_range[:-1])

                    if unit == 'm': #menit
                        time_threshold = now() - timedelta(minutes = value)
                    elif unit == 'h': #jam
                        time_threshold = now() - timedelta(hours = value)
                    elif unit == 'd' : #hari
                        time_threshold = now() - timedelta(days = value)
            
                    else:
                        raise ValueError("Satuan waktu tidak valid")
                
                queryset = queryset.filter(timestamp__gte=time_threshold)
                    
            except (ValueError, TypeError):
                raise ValidationError ({"error": "format time_range tidak valid"})
                
        return queryset.order_by('-timestamp')
   
    



# Retrive specific history
class DataAyamHistoryDetail(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataAyamHistorySerializer
    def get_queryset(self):
        # Return all records with the given data_ayam_id
        pk = self.kwargs.get("pk")

        if not pk:
            return DataAyamHistory.objects.none()
        
        queryset = DataAyamHistory.objects.filter(data_ayam_id=pk)
        time_range = self.request.query_params.get('time_range', None)

        if time_range:
            #unit waktu (m = menit, h = jam, d = hari, mo = bulan)
            try:
                if time_range.endswith("mo") : #bulan
                    value = int(time_range[:-2])
                    time_threshold = now() - timedelta(days = value * 30)
                else:
                    unit = time_range[-1]
                    value = int(time_range[:-1])

                    if unit == 'm': #menit
                        time_threshold = now() - timedelta(minutes = value)
                    elif unit == 'h': #jam
                        time_threshold = now() - timedelta(hours = value)
                    elif unit == 'd' : #hari
                        time_threshold = now() - timedelta(days = value)
            
                    else:
                        raise ValueError("Satuan waktu tidak valid")
                
                queryset = queryset.filter(timestamp__gte=time_threshold)
                    
            except (ValueError, TypeError):
                raise ValidationError ({"error": "format time_range tidak valid"})
                
        return queryset.order_by('-timestamp')



class CommandView(APIView):
    #API untuk mengirim perinah
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        #method untuk esp32 meminta perintah
        #Hanya entitas pengguna dengan role "alat" yang bisa menggunakan API view ini
        if request.user.role.lower() != 'alat':
            return Response({"error": "Akses tidak diizinkan kecuali untuk alat"})
        else:
            command = cache.get(f"esp32_command_{request.user.id}", None)
            return Response({"command": command})

    def post(self, request):
        #Only authorized commands to esp32

        if request.user.role.lower() not in ["pemilik", "staf"]:
            return Response({"error": "Hanya pemilik atau staff yang dapat mengirim perintah"})
        
        user_id = request.data.get("user_id")
        command = request.data.get("command")

        #Validate user ID

        try:
            alat = CustomUser.objects.get(id=user_id, role_iexact="alat")

        except CustomUser.DoesNotExist:
            return Response({"error": "alat tidak ditemukan"}, status=404)

        if command not in ["wake", "sleep"]:
            return Response({"error": "Perintah tidak valid, gunakan 'wake' atau 'sleep'"})
    
        #Store command in cache
        cache.set(f"esp32_command_{alat.id}", command, timeout=300) #simpan buat 5 menit

        return Response({"message": f"Perintah '{command}' dikirim ke {alat.username}"})
    
class AlatCreateUpdateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAlatRole]
    serializer_class = AlatSerializer

class AlatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Alat.objects.all()
    serializer_class = AlatSerializer


