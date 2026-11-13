from django.db import models #DJANGO NUN VERİTABANI SİSTEMİ
from django.contrib.auth.models import User #hazır kullanıcı modeli

class EmissionRecord(models.Model): #yeni veritabanı tablosu

    user = models.ForeignKey(User, on_delete=models.CASCADE) #kayıt hangi kullanıcıya ait,kullanıcı silinirse kayıtları da silinir.

    #girilen veriler
    electricity = models.FloatField(default=0)
    natural_gas = models.FloatField(default=0)
    fuel_type = models.CharField(max_length=20, default="benzin")
    fuel_amount = models.FloatField(default=0)

    #hesaplanan değerler
    scope1 = models.FloatField(default=0)
    scope2 = models.FloatField(default=0)

    total_emission = models.FloatField(default=0)

    #kayıt oluşturulduğunda tarih ve saat otomatik yazılır.
    created_at = models.DateTimeField(auto_now_add=True)