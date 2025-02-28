from rest_framework import generics
from .models import Parameter
from .serializers import ParameterSerializer
from .models import DataAyam
from .serializers import DataAyamSerializer
from rest_framework.response import Response
from .models import DataAyam, DataAyamHistory
from .serializers import DataAyamSerializer
from rest_framework import status
from .serializers import DataAyamHistorySerializer
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework import serializers
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.core.cache import cache

class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)
    

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)


# List and Create Parameter
class ParameterListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer

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
    
# List and Create Parameter
class DataAyamListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataAyam.objects.all()
    serializer_class = DataAyamSerializer

# Bulk or delete all
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

# Retrieve, Update, and Delete specific Parameter
class DataAyamDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
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
            # DataAyamHistory.objects.create(data_ayam = instance)

        # Simpan perubahan
        self.perform_update(serializer)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#List or create all
class DataAyamHistoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataAyamHistory.objects.all()
    serializer_class = DataAyamHistorySerializer

    #def get_queryset(self):
    #    pk = self.kwargs.get("pk")
    #    if pk is None:
    #        return DataAyamHistory.objects.none()
    #    return DataAyamHistory.objects.filter(data_ayam_id = pk).order_by("-timestamp")
    



# Retrive and delete specific history
class DataAyamHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataAyamHistory.objects.all()
    serializer_class = DataAyamHistorySerializer




class CommandView(APIView):
    #API untuk mengirim perinah
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        #method untuk esp32 meminta perintah
        #Only users with the role 'alat' or 'Alat' can use this APIView
        if request.user.role.lower() != 'alat':
            return Response({"error": "Akses tidak diizinkan kecuali untuk alat"})
        else:
            command = cache.get(f"esp32_command_{request.user.id}", None)
            return Response({"command": command})

    def post(self, request):
        #Only authorized commands to esp32

        if request.user.role not in ["pemilik", "Pemilik", "Staf", "staf"]:
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