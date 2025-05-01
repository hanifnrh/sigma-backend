from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from api.models import CustomUser, Parameter


@receiver(post_save, sender=Parameter)
def send_email_alert(sender, instance, created, **kwargs):
    
    if instance.status == "Bahaya":
        recipients = CustomUser.objects.filter(role__in=["staf", "pemilik"]).values_list('email', flat=True)
        recipiets = list(filter(None, recipients))

        if recipients:
            floor = dict(Parameter.FLOOR_CHOICES).get(instance.floor, "Floor tidak diketahui")

            send_mail(
                subject=f"PERHATIAN! LEVEL PARAMETER KANDANG DALAM BAHAYA",
                message = (
                    f"Parameter berikut telah mencapai level bahaya di lantai {floor}\n\n"
                    f"Ammonia: {instance.ammonia} (Status: {'Bahaya' if instance.ammonia > 30 else 'Tidak dalam bahaya'})\n\n"
                    f"Temperatur: {instance.temperature} derajat celcius (Status: {'Bahaya' if instance.temperature < 18 or instance.temperature > 36 else 'Tidak dalam bahaya' })\n\n"
                    f"Kelembapan: {instance.humidity}% (Status: {'Bahaya' if instance.humidity < 58 or instance.humidity > 72 else 'Not Bahaya'})\n\n"
                    f"Harap melakukan aksi tanggap"
                ),
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently = False,
            )