from django.contrib import admin
from .models import Parameter, DataAyam, DataAyamHistory, CustomUser, Alat
# Register your models here.
admin.site.register(Parameter)
admin.site.register(DataAyam)
admin.site.register(DataAyamHistory)
admin.site.register(Alat)
admin.site.register(CustomUser)