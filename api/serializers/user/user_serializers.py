from rest_framework import serializers
from api.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'password', 'profile_picture', 'full_name')
        extra_kwargs = {
             'password': {'write_only': True} #Pastikan password tidak bocor di response.
        }
    

    def __init__(self, *args, **kwargs):
        #field ini digunakan untuk filter request body response
        #jadi ketika kelas serializer ini dipanggil bisa menggunakan argumen field untuk menyaring field apa yang mau ditampilkan dalam response 
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
             allowed = set(fields)
             existing = set(self.fields)
             for field_name in existing - allowed:
                  self.fields.pop(field_name)

    def create(self, validated_data):
        #registrasi pengguna
        #Paksa role ke tamu dalam request body
        validated_data['role'] = 'tamu'
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        #mengatur pembaruan profile dan pergantian password
        
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if password:
             instance.set_password(password)

        instance.save()

        return instance