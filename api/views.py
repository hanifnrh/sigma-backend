from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Parameter,
    DataAyam,
    DataAyamHistory,
    CustomUser
)
from .serializers import (
    ParameterSerializer,
    DataAyamSerializer,
    DataAyamHistorySerializer,
    UserSerializer,
    UserRegisterSerializer
)
from .permissions import IsOwner, IsStaff
import logging

logger = logging.getLogger(__name__)
class LoginView(APIView):
   def post(self, request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    print(f"DEBUG - Authenticate User: {user}")  # Cek apakah user terautentikasi
    if user:
        print(f"DEBUG - User Type: {type(user)}")  # Pastikan ini CustomUser
        print(f"DEBUG - User ID: {user.id}, Role: {user.role}")  # Debugging role

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,  # Pastikan role ada
            }
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
from rest_framework_simplejwt.exceptions import InvalidToken

class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({'access': new_access_token})
        except InvalidToken:
            return Response({'error': 'Invalid refresh token'}, status=400)

class OwnerOnlyView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        return Response({"message": "Welcome, Owner!"})

class StaffOnlyView(APIView):
    permission_classes = [IsStaff]

    def get(self, request):
        return Response({"message": "Welcome, Staff!"})

# List and Create Parameter
class ParameterListCreate(generics.ListCreateAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    
    def delete(self, request, *args, **kwargs):
        # Menghapus seluruh data parameter
        Parameter.objects.all().delete()
        return Response({"message": "All parameters have been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)  

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
