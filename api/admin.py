from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Parameter, DataAyam, DataAyamHistory, CustomUser, Alat
# Register your models here
# Class admin digunakan untuk memperbaiki display model di django admin
class ParameterAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameter'

class AlatAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key',)
    list_display = ('alat_id', 'api_key')
    fields = ('alat_id', 'api_key')  # secara eksplisit tampilkan API key


class ParameterAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'ammonia',
        'temperature',
        'humidity',
        'floor',
        'score',
        'status',
    )
    list_filter = ('floor', 'status')
    ordering = ('-timestamp',)



class DataAyamAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'jumlah_ayam_awal',
        'tanggal_mulai',
        'tanggal_panen',
        'jumlah_ayam',
        'mortalitas',
        'usia_ayam',
    )
    list_filter = ('tanggal_mulai', 'tanggal_panen')
    ordering = ('-timestamp',)


class DataAyamHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'jumlah_ayam_awal',
        'tanggal_mulai',
        'tanggal_panen',
        'jumlah_ayam',
        'mortalitas',
        'usia_ayam',
        
    )
    list_filter = ('tanggal_mulai', 'tanggal_panen')
    ordering = ('-timestamp',)

class UserAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'
    list_display = ('full_name', 'username', 'email', 'role', 'is_approved', 'profile_picture')
    list_filter = ('role', 'is_approved')
    

    actions = ['approve_pengguna', 'cabut_approval_pengguna']

    def approve_pengguna(self, request, queryset):
        queryset.update(is_approved=True) #Berikan approval
    
    def cabut_approval_pengguna(self, request, queryset):
        queryset.update(is_approved=False) #Cabut approval

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data: #hash password sebelum kirim ke basis data supaya bekerja dengan sistem otentikasi.
            obj.set_password(obj.password)
        obj.save()

    


admin.site.register(Parameter, ParameterAdmin)
admin.site.register(DataAyam, DataAyamAdmin)
admin.site.register(DataAyamHistory, DataAyamHistoryAdmin)
admin.site.register(Alat, AlatAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.site_header = 'SIGMA ADMIN'
admin.site.site_title = 'Portal administrasi SIGMA'
admin.site.index_title = 'Selamat datang ke administrasi SIGMA!'