from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from klinik.models import Hasta, TibbiKayit


class Command(BaseCommand):
    help = "CSV dosyasinin ilk satirlarindan Hasta ve TibbiKayit tohum verisi olusturur."

    def add_arguments(self, parser):
        parser.add_argument(
            "--satir-sayisi",
            type=int,
            default=15,
            help="Tohumlama icin okunacak ilk satir sayisi (varsayilan: 15).",
        )

    def _veri_dosyasi_yolu(self):
        komut_dosyasi = Path(__file__).resolve()
        proje_koku = komut_dosyasi.parents[4]
        return proje_koku / "heart_failure_clinical_records_dataset.csv"

    def _dogum_tarihi_hesapla(self, yas):
        bugun = date.today()
        return bugun - timedelta(days=int(yas) * 365)

    def _tc_kimlik_no_uret(self, satir_indeksi):
        return f"9{satir_indeksi + 1000000000:010d}"

    def _telefon_uret(self, satir):
        # Telefon degeri dogrudan satirdaki iki sayisal alandan turetilir.
        tumleyen = int(float(satir["serum_sodium"])) % 100
        baz = int(float(satir["time"])) % 10000000
        return f"05{tumleyen:02d}{baz:07d}"

    @transaction.atomic
    def handle(self, *args, **options):
        veri_yolu = self._veri_dosyasi_yolu()
        if not veri_yolu.exists():
            self.stderr.write(self.style.ERROR(f"Veri dosyasi bulunamadi: {veri_yolu}"))
            return

        satir_sayisi = max(1, int(options["satir_sayisi"]))
        veri = pd.read_csv(veri_yolu).head(satir_sayisi)

        olusturulan_hasta = 0
        olusturulan_kayit = 0

        for satir_indeksi, (_, satir) in enumerate(veri.iterrows()):
            yas = int(float(satir["age"]))
            cinsiyet = "Erkek" if int(float(satir["sex"])) == 1 else "Kadin"

            hasta, yeni_hasta = Hasta.objects.get_or_create(
                tc_kimlik_no=self._tc_kimlik_no_uret(satir_indeksi),
                defaults={
                    "ad_soyad": f"CSV Hasta {satir_indeksi + 1}",
                    "dogum_tarihi": self._dogum_tarihi_hesapla(yas),
                    "cinsiyet": cinsiyet,
                    "telefon": self._telefon_uret(satir),
                },
            )
            if yeni_hasta:
                olusturulan_hasta += 1

            _, yeni_kayit = TibbiKayit.objects.get_or_create(
                hasta=hasta,
                yas=yas,
                anemi=bool(int(float(satir["anaemia"]))),
                kreatinin_fosfokinaz=float(satir["creatinine_phosphokinase"]),
                diyabet=bool(int(float(satir["diabetes"]))),
                ejeksiyon_fraksiyonu=float(satir["ejection_fraction"]),
                yuksek_tansiyon=bool(int(float(satir["high_blood_pressure"]))),
                trombosit=float(satir["platelets"]),
                serum_kreatinin=float(satir["serum_creatinine"]),
                serum_sodyum=float(satir["serum_sodium"]),
                cinsiyet_erkek=bool(int(float(satir["sex"]))),
                sigara=bool(int(float(satir["smoking"]))),
                takip_suresi=int(float(satir["time"])),
            )
            if yeni_kayit:
                olusturulan_kayit += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Tohumlama tamamlandi. Yeni hasta: {olusturulan_hasta}, yeni tibbi kayit: {olusturulan_kayit}"
            )
        )
