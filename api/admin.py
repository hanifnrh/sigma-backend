from django.contrib import admin
from .models import Parameter, DataAyam, DataAyamHistory, CustomUser, Alat
# Register your models here
# Class admin digunakan untuk memperbaiki display model di django admin
class ParameterAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameter'

class AlatAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key',)
    list_display = ('alat_id', 'battery_level', 'api_key')
    fields = ('alat_id', 'battery_level', 'status', 'api_key')  # secara eksplisit tampilkan API key

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
    list_display = ('full_name', 'username', 'email', 'role', 'is_approved', 'profile_picture')
    list_filter = ('role', 'is_approved')

    actions = ['approve_pengguna', 'cabut_approval_pengguna']

    def approve_pengguna(self, request, queryset):
        queryset.update(is_approved=True, role = 'staff') #Ganti role ke staff ketika approve
    
    def cabut_approval_pengguna(self, request, queryset):
        queryset.update(is_approved=False, role = 'tamu') #Ganti role ke tamu jika mencabut approval



admin.site.register(Parameter, ParameterAdmin)
admin.site.register(DataAyam, DataAyamAdmin)
admin.site.register(DataAyamHistory, DataAyamHistoryAdmin)
admin.site.register(Alat, AlatAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.site_header = 'SIGMA ADMIN'
admin.site.site_title = 'Portal administrasi SIGMA'
admin.site.index_title = 'Selamat datang ke administrasi SIGMA!'