import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigma_backend.settings')

import django
from django.utils import timezone
django.setup()


import random
from api.models import CustomUser, Parameter, DataAyam, DataAyamHistory

from faker import Faker

fake = Faker()

timestamp = fake.date_time()
timestamp = timezone.make_aware(timestamp)


def add_dataAyam():
    d = DataAyam.objects.get_or_create(timestamp = timestamp, jumlah_ayam_awal = random.randint(100, 1000), tanggal_mulai = fake.date(), tanggal_panen = fake.date(), jumlah_ayam = random.randint(0, 1000), mortalitas = random.random(), usia_ayam = random.randint(0, 30))[0]
    d.save()

    return d

def populate(n = 10):

    for entry in range(n):
    #get data ayam
        da = add_dataAyam()
        
        #create fake DataAyamHistory

        data_ah = DataAyamHistory.objects.get_or_create(data_ayam = da, jumlah_ayam_awal = random.randint(100, 1000), jumlah_ayam = random.randint(0, 1000), tanggal_mulai = fake.date(), tanggal_panen = fake.date(), mortalitas = random.random(), timestamp = timestamp, usia_ayam = random.randint(0, 30))[0]

        parameter = Parameter.objects.get_or_create(ammonia = random.uniform(0, 30), temperature = random.uniform(0, 30), humidity = random.random(), score = random.randint(0, 100))[0]


    

    #create some fake data for entry

if __name__ == "__main__":
    print("Populating the DB")
    populate(10)
    print("Populating complete")