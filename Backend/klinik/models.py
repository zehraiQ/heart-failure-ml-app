from django.db import models


class Hasta(models.Model):
    ad_soyad = models.CharField(max_length=120, verbose_name="Ad Soyad")
    tc_kimlik_no = models.CharField(max_length=11, unique=True, verbose_name="TC Kimlik No")
    dogum_tarihi = models.DateField(verbose_name="Dogum Tarihi")
    cinsiyet = models.CharField(max_length=10, verbose_name="Cinsiyet")
    telefon = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Olusturma Tarihi")

    class Meta:
        verbose_name = "Hasta"
        verbose_name_plural = "Hastalar"
        ordering = ["-olusturma_tarihi"]

    @property
    def son_tibbi_kayit(self):
        return self.tibbi_kayitlar.first()

    def __str__(self):
        return f"{self.ad_soyad} ({self.tc_kimlik_no})"


class Doktor(models.Model):
    ad_soyad = models.CharField(max_length=120, verbose_name="Ad Soyad")
    uzmanlik_alani = models.CharField(max_length=120, verbose_name="Uzmanlik Alani")
    eposta = models.EmailField(unique=True, verbose_name="E-Posta")
    telefon = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    aktif_mi = models.BooleanField(default=True, verbose_name="Aktif mi")

    class Meta:
        verbose_name = "Doktor"
        verbose_name_plural = "Doktorlar"
        ordering = ["ad_soyad"]

    def __str__(self):
        return f"Dr. {self.ad_soyad}"


class Randevu(models.Model):
    durum_secenekleri = (
        ("planlandi", "Planlandi"),
        ("iptal", "Iptal"),
        ("tamamlandi", "Tamamlandi"),
    )
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE, related_name="randevular", verbose_name="Hasta")
    doktor = models.ForeignKey(Doktor, on_delete=models.CASCADE, related_name="randevular", verbose_name="Doktor")
    randevu_tarihi = models.DateTimeField(verbose_name="Randevu Tarihi")
    notlar = models.TextField(blank=True, verbose_name="Notlar")
    durum = models.CharField(max_length=20, choices=durum_secenekleri, default="planlandi", verbose_name="Durum")

    class Meta:
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"
        ordering = ["-randevu_tarihi"]

    def __str__(self):
        return f"{self.hasta.ad_soyad} - {self.doktor.ad_soyad}"


class TibbiKayit(models.Model):
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE, related_name="tibbi_kayitlar", verbose_name="Hasta")
    yas = models.PositiveIntegerField(verbose_name="Yas")
    anemi = models.BooleanField(verbose_name="Anemi")
    kreatinin_fosfokinaz = models.FloatField(verbose_name="Kreatinin Fosfokinaz")
    diyabet = models.BooleanField(verbose_name="Diyabet")
    ejeksiyon_fraksiyonu = models.FloatField(verbose_name="Ejeksiyon Fraksiyonu")
    yuksek_tansiyon = models.BooleanField(verbose_name="Yuksek Tansiyon")
    trombosit = models.FloatField(verbose_name="Trombosit")
    serum_kreatinin = models.FloatField(verbose_name="Serum Kreatinin")
    serum_sodyum = models.FloatField(verbose_name="Serum Sodyum")
    cinsiyet_erkek = models.BooleanField(verbose_name="Cinsiyet Erkek")
    sigara = models.BooleanField(verbose_name="Sigara")
    takip_suresi = models.PositiveIntegerField(verbose_name="Takip Suresi")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayit Tarihi")

    class Meta:
        verbose_name = "Tibbi Kayit"
        verbose_name_plural = "Tibbi Kayitlar"
        ordering = ["-kayit_tarihi"]

    def __str__(self):
        return f"{self.hasta.ad_soyad} - {self.kayit_tarihi.date()}"


class TahminSonucu(models.Model):
    tibbi_kayit = models.ForeignKey(TibbiKayit, on_delete=models.CASCADE, related_name="tahmin_sonuclari", verbose_name="Tibbi Kayit")
    karar_agaci_tahmini = models.BooleanField(verbose_name="Karar Agaci Tahmini")
    knn_tahmini = models.BooleanField(verbose_name="KNN Tahmini")
    naive_bayes_tahmini = models.BooleanField(verbose_name="Naive Bayes Tahmini")
    rastgele_orman_tahmini = models.BooleanField(verbose_name="Rastgele Orman Tahmini")
    lojistik_regresyon_tahmini = models.BooleanField(verbose_name="Lojistik Regresyon Tahmini")
    toplu_tahmin = models.BooleanField(verbose_name="Toplu Tahmin")
    olasilik = models.FloatField(default=0.0, verbose_name="Olasilik")
    tahmin_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Tahmin Tarihi")

    class Meta:
        verbose_name = "Tahmin Sonucu"
        verbose_name_plural = "Tahmin Sonuclari"
        ordering = ["-tahmin_tarihi"]

    def __str__(self):
        return f"Tahmin #{self.id} - {self.tibbi_kayit.hasta.ad_soyad}"
