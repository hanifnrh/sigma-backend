from django.contrib import admin
from .models import Parameter, DataAyam, DataAyamHistory, CustomUser, Alat
# Register your models here
# Class admin digunakan untuk memperbaiki display model di django admin
class ParameterAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameter'

class AlatAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Alat'
        verbose_name_plural = 'Alat'


class DataAyamAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Data ayam'
        verbose_name_plural = 'Data ayam'

class DataAyamAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Data ayam'
        verbose_name_plural = 'Data ayam'

class DataAyamHistoryAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'Riwayat data ayam'
        verbose_name_plural = 'Riwayat data ayam'

class UserAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'



admin.site.register(Parameter, ParameterAdmin)
admin.site.register(DataAyam, DataAyamAdmin)
admin.site.register(DataAyamHistory, DataAyamHistoryAdmin)
admin.site.register(Alat, AlatAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.site_header = 'SIGMA ADMIN'
admin.site.site_title = 'Portal administrasi SIGMA'
admin.site.index_title = 'Selamat datang ke administrasi SIGMA!'