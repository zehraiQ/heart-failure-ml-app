import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from ai_entegrasyon import tahmin_hesapla

from .forms import DoktorForm, HastaForm, RandevuForm, TahminForm
from .models import Doktor, Hasta, Randevu, TahminSonucu, TibbiKayit


def _ikili_tahminden_risk_etiketi(ikili_tahmin):
    """Veritabaninda bool saklanan tahminleri arayuzde High Risk / Low Risk olarak sunar."""
    return "High Risk" if ikili_tahmin else "Low Risk"


def _tahmin_sonucu_sunum_sozlugu(sonuc):
    """TahminSonucu ORM nesnesinden sablon icin metin etiketleri uretilir."""
    return {
        "karar_agaci": _ikili_tahminden_risk_etiketi(sonuc.karar_agaci_tahmini),
        "knn": _ikili_tahminden_risk_etiketi(sonuc.knn_tahmini),
        "naive_bayes": _ikili_tahminden_risk_etiketi(sonuc.naive_bayes_tahmini),
        "rastgele_orman": _ikili_tahminden_risk_etiketi(sonuc.rastgele_orman_tahmini),
        "lojistik_regresyon": _ikili_tahminden_risk_etiketi(sonuc.lojistik_regresyon_tahmini),
        "toplu": _ikili_tahminden_risk_etiketi(sonuc.toplu_tahmin),
    }


def _ortak_sayfa_bilgisi():
    """Tum sayfalarda kullanilan temel menu istatistiklerini dondurur (ORM sayimlari)."""
    return {
        "menu_toplam_hasta": Hasta.objects.count(),
        "menu_toplam_doktor": Doktor.objects.count(),
        "menu_toplam_randevu": Randevu.objects.count(),
        "menu_toplam_tahmin": TahminSonucu.objects.count(),
    }


def ana_sayfa_view(request):
    # Dashboard kartlari ve menu sayaclari ayni ORM sayimlarini kullanir (tek kaynak).
    toplam_hasta = Hasta.objects.count()
    toplam_doktor = Doktor.objects.count()
    toplam_randevu = Randevu.objects.count()
    toplam_tahmin = TahminSonucu.objects.count()
    baglam = {
        "menu_toplam_hasta": toplam_hasta,
        "menu_toplam_doktor": toplam_doktor,
        "menu_toplam_randevu": toplam_randevu,
        "menu_toplam_tahmin": toplam_tahmin,
        "dashboard_toplam_hasta": toplam_hasta,
        "dashboard_toplam_doktor": toplam_doktor,
        "dashboard_toplam_randevu": toplam_randevu,
        "dashboard_toplam_tahmin": toplam_tahmin,
        "son_randevular": Randevu.objects.select_related("hasta", "doktor").all()[:5],
        "son_tahminler": TahminSonucu.objects.select_related("tibbi_kayit__hasta").all()[:5],
    }
    return render(request, "ana_sayfa.html", baglam)


@require_http_methods(["GET", "POST"])
def hasta_ekle_view(request):
    form = HastaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hasta basariyla eklendi.")
        return redirect("hasta_listesi")
    return render(request, "hasta_ekle.html", {"form": form, **_ortak_sayfa_bilgisi()})


@require_http_methods(["GET", "POST"])
def hasta_duzenle_view(request, hasta_id):
    hasta = get_object_or_404(Hasta, pk=hasta_id)
    form = HastaForm(request.POST or None, instance=hasta)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hasta bilgileri guncellendi.")
        return redirect("hasta_listesi")
    return render(
        request,
        "hasta_duzenle.html",
        {"form": form, "hasta": hasta, **_ortak_sayfa_bilgisi()},
    )


@require_http_methods(["GET", "POST"])
def hasta_sil_view(request, hasta_id):
    hasta = get_object_or_404(Hasta, pk=hasta_id)
    if request.method == "POST":
        hasta.delete()
        messages.success(request, "Hasta silindi.")
        return redirect("hasta_listesi")
    return render(request, "hasta_sil_onay.html", {"hasta": hasta, **_ortak_sayfa_bilgisi()})


def hasta_listesi_view(request):
    hastalar = Hasta.objects.all()
    return render(request, "hasta_listesi.html", {"hastalar": hastalar, **_ortak_sayfa_bilgisi()})


@require_http_methods(["GET", "POST"])
def doktor_ekle_view(request):
    form = DoktorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Doktor basariyla eklendi.")
        return redirect("doktor_listesi")
    return render(
        request,
        "doktor_ekle.html",
        {"form": form, "sayfa_basligi": "Doktor Ekle", **_ortak_sayfa_bilgisi()},
    )


@require_http_methods(["GET", "POST"])
def doktor_duzenle_view(request, doktor_id):
    doktor = get_object_or_404(Doktor, pk=doktor_id)
    form = DoktorForm(request.POST or None, instance=doktor)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Doktor bilgileri guncellendi.")
        return redirect("doktor_listesi")
    return render(
        request,
        "doktor_duzenle.html",
        {"form": form, "doktor": doktor, **_ortak_sayfa_bilgisi()},
    )


@require_http_methods(["GET", "POST"])
def doktor_sil_view(request, doktor_id):
    doktor = get_object_or_404(Doktor, pk=doktor_id)
    if request.method == "POST":
        doktor.delete()
        messages.success(request, "Doktor silindi.")
        return redirect("doktor_listesi")
    return render(request, "doktor_sil_onay.html", {"doktor": doktor, **_ortak_sayfa_bilgisi()})


def doktor_listesi_view(request):
    doktorlar = Doktor.objects.all()
    if request.GET.get("format") == "json":
        doktorlar_json = list(
            doktorlar.values("id", "ad_soyad", "uzmanlik_alani", "eposta", "aktif_mi")
        )
        return JsonResponse({"doktorlar": doktorlar_json})
    return render(request, "doktor_listesi.html", {"doktorlar": doktorlar, **_ortak_sayfa_bilgisi()})


@require_http_methods(["GET", "POST"])
def randevu_olustur_view(request):
    form = RandevuForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Randevu olusturuldu.")
        return redirect("randevu_listesi")
    return render(
        request,
        "randevu_olustur.html",
        {"randevu_formu": form, **_ortak_sayfa_bilgisi()},
    )


def randevu_listesi_view(request):
    randevular = Randevu.objects.select_related("hasta", "doktor").all()
    return render(request, "randevu_listesi.html", {"randevular": randevular, **_ortak_sayfa_bilgisi()})


@require_http_methods(["POST"])
def randevu_iptal_view(request, randevu_id):
    randevu = get_object_or_404(Randevu, id=randevu_id)
    randevu.durum = "iptal"
    randevu.save(update_fields=["durum"])
    messages.info(request, "Randevu iptal edildi.")
    return redirect("randevu_listesi")


@require_http_methods(["GET", "POST"])
def tahmin_yap_view(request):
    form = TahminForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                sozluk = form.temizlenmis_biyobelirtec_sozlugu()
                hasta = sozluk.pop("hasta")
                vektor = form.tahmin_vektoru()
                tibbi_kayit = TibbiKayit.objects.create(hasta=hasta, **sozluk)
                tahmin = tahmin_hesapla(vektor)
                sonuc = TahminSonucu.objects.create(
                    tibbi_kayit=tibbi_kayit,
                    karar_agaci_tahmini=bool(tahmin["karar_agaci"]),
                    knn_tahmini=bool(tahmin["knn"]),
                    naive_bayes_tahmini=bool(tahmin["naive_bayes"]),
                    rastgele_orman_tahmini=bool(tahmin["rastgele_orman"]),
                    lojistik_regresyon_tahmini=bool(tahmin["lojistik_regresyon"]),
                    toplu_tahmin=bool(tahmin["toplu_tahmin"]),
                    olasilik=tahmin["olasilik"],
                )

                eylem = request.POST.get("eylem")
                if eylem == "kaydet_ve_goruntule":
                    messages.success(request, f"Tahmin kaydedildi — {hasta.ad_soyad} profiline yonlendiriliyorsunuz.")
                    return redirect("hasta_profil", hasta_id=hasta.id)

                messages.success(request, "Tahmin basariyla olusturuldu.")
                return render(
                    request,
                    "tahmin_yap.html",
                    {
                        "tahmin_formu": TahminForm(),
                        "tahmin_sonucu": sonuc,
                        "tahmin_sunumu": _tahmin_sonucu_sunum_sozlugu(sonuc),
                        **_ortak_sayfa_bilgisi(),
                    },
                )
            except (ValueError, ValidationError, KeyError) as hata:
                messages.error(
                    request,
                    f"Tahmin sirasinda hata olustu: {hata}",
                )
        else:
            messages.error(request, "Lutfen asagidaki hatalari duzeltin.")

        return render(
            request,
            "tahmin_yap.html",
            {
                "tahmin_formu": form,
                **_ortak_sayfa_bilgisi(),
            },
        )

    return render(
        request,
        "tahmin_yap.html",
        {
            "tahmin_formu": form,
            **_ortak_sayfa_bilgisi(),
        },
    )


@require_http_methods(["GET"])
def hasta_son_kayit_json(request, hasta_id):
    hasta = get_object_or_404(Hasta, pk=hasta_id)
    kayit = hasta.son_tibbi_kayit
    if not kayit:
        return JsonResponse({"bulundu": False})
    return JsonResponse({
        "bulundu": True,
        "veri": {
            "yas": kayit.yas,
            "anemi": "1" if kayit.anemi else "0",
            "kreatinin_fosfokinaz": kayit.kreatinin_fosfokinaz,
            "diyabet": "1" if kayit.diyabet else "0",
            "ejeksiyon_fraksiyonu": kayit.ejeksiyon_fraksiyonu,
            "yuksek_tansiyon": "1" if kayit.yuksek_tansiyon else "0",
            "trombosit": kayit.trombosit,
            "serum_kreatinin": kayit.serum_kreatinin,
            "serum_sodyum": kayit.serum_sodyum,
            "cinsiyet_erkek": "1" if kayit.cinsiyet_erkek else "0",
            "sigara": "1" if kayit.sigara else "0",
            "takip_suresi": kayit.takip_suresi,
        },
    })


@require_http_methods(["GET"])
def hasta_gecmis_json(request, hasta_id):
    hasta = get_object_or_404(Hasta, pk=hasta_id)
    kayitlar = hasta.tibbi_kayitlar.prefetch_related("tahmin_sonuclari").order_by("kayit_tarihi")

    veri = []
    for kayit in kayitlar:
        tahmin = kayit.tahmin_sonuclari.first()
        snapshot = {
            "id": kayit.id,
            "tarih": kayit.kayit_tarihi.isoformat(),
            "yas": kayit.yas,
            "anemi": 1 if kayit.anemi else 0,
            "kreatinin_fosfokinaz": kayit.kreatinin_fosfokinaz,
            "diyabet": 1 if kayit.diyabet else 0,
            "ejeksiyon_fraksiyonu": kayit.ejeksiyon_fraksiyonu,
            "yuksek_tansiyon": 1 if kayit.yuksek_tansiyon else 0,
            "trombosit": kayit.trombosit,
            "serum_kreatinin": kayit.serum_kreatinin,
            "serum_sodyum": kayit.serum_sodyum,
            "cinsiyet_erkek": 1 if kayit.cinsiyet_erkek else 0,
            "sigara": 1 if kayit.sigara else 0,
            "takip_suresi": kayit.takip_suresi,
        }
        if tahmin:
            snapshot["toplu_tahmin"] = 1 if tahmin.toplu_tahmin else 0
            snapshot["olasilik"] = round(tahmin.olasilik, 3)
        veri.append(snapshot)

    return JsonResponse({
        "hasta": hasta.ad_soyad,
        "hasta_id": hasta.id,
        "kayitlar": veri,
    })


def hasta_profil_view(request, hasta_id):
    hasta = get_object_or_404(Hasta, pk=hasta_id)
    return render(request, "hasta_profil.html", {
        "hasta": hasta,
        **_ortak_sayfa_bilgisi(),
    })


def gecmis_tahminler_view(request):
    sonuc_listesi = list(
        TahminSonucu.objects.select_related("tibbi_kayit__hasta").values(
            "id",
            "tibbi_kayit__hasta__ad_soyad",
            "toplu_tahmin",
            "olasilik",
            "tahmin_tarihi",
        )[:100]
    )
    return JsonResponse({"gecmis_tahminler": sonuc_listesi})
