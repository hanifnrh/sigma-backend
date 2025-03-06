from rest_framework import serializers
from api.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
    
    def validate(self, attrs):
        role = attrs.get('role', 'staf')
        email = attrs.get('email', None)

        if role in ['staf', 'pemilik'] and not email:
            raise serializers.ValidationError({"email": "staff dan pemilik harus memiliki email" })

        return attrs
    
    def create(self, validated_data):

        role = validated_data.get('role', 'staf')

        if role == 'alat':
            validated_data.pop('email', None)

        user = CustomUser.objects.create_user(**validated_data)

        return user
    
class ProfilePictureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        #handle profile picture update
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance