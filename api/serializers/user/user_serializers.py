from rest_framework import serializers
from api.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'password', 'profile_picture', 'full_name')

    
    def create(self, validated_data):
        #registrasi pengguna
        role = validated_data.get('role', 'staf')

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