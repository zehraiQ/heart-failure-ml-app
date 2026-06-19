from django.contrib import admin

from .models import Doktor, Hasta, Randevu, TahminSonucu, TibbiKayit


@admin.register(Hasta)
class HastaYonetim(admin.ModelAdmin):
    list_display = ("ad_soyad", "tc_kimlik_no", "dogum_tarihi", "cinsiyet")
    search_fields = ("ad_soyad", "tc_kimlik_no")


@admin.register(Doktor)
class DoktorYonetim(admin.ModelAdmin):
    list_display = ("ad_soyad", "uzmanlik_alani", "eposta", "aktif_mi")
    list_filter = ("aktif_mi",)


@admin.register(Randevu)
class RandevuYonetim(admin.ModelAdmin):
    list_display = ("hasta", "doktor", "randevu_tarihi", "durum")
    list_filter = ("durum",)


@admin.register(TibbiKayit)
class TibbiKayitYonetim(admin.ModelAdmin):
    list_display = ("hasta", "yas", "serum_kreatinin", "serum_sodyum", "kayit_tarihi")


@admin.register(TahminSonucu)
class TahminSonucuYonetim(admin.ModelAdmin):
    list_display = ("tibbi_kayit", "toplu_tahmin", "olasilik", "tahmin_tarihi")
