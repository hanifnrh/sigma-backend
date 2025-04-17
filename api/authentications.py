from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Alat

class AlatAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return None
        
        try:
            alat = Alat.objects.get(api_key = api_key)

        except Alat.DoesNotExist:
            raise AuthenticationFailed('API Key tidak valid')
        
        #Karena DRF meminta (user, auth) return dan alat bukan merupakan user,
        #Kita akali dengan return alat sebagai user dan None sebagai Auth
        return (alat, None)