from pathlib import Path

import joblib
import numpy as np


MODEL_DIZINI = Path(__file__).resolve().parent.parent / "YapayZeka_Modulu"

SCALER_DOSYASI = MODEL_DIZINI / "olcekleyici.pkl"
KARAR_AGACI_DOSYASI = MODEL_DIZINI / "karar_agaci.pkl"
KNN_DOSYASI = MODEL_DIZINI / "knn.pkl"
NAIVE_BAYES_DOSYASI = MODEL_DIZINI / "naive_bayes.pkl"
RASTGELE_ORMAN_DOSYASI = MODEL_DIZINI / "rastgele_orman.pkl"
LOJISTIK_DOSYASI = MODEL_DIZINI / "lojistik_regresyon.pkl"


def _modelleri_yukle():
    """Tahmin asamasinda kullanilacak tum modelleri bir kez yukler."""
    return {
        "olcekleyici": joblib.load(SCALER_DOSYASI),
        "karar_agaci": joblib.load(KARAR_AGACI_DOSYASI),
        "knn": joblib.load(KNN_DOSYASI),
        "naive_bayes": joblib.load(NAIVE_BAYES_DOSYASI),
        "rastgele_orman": joblib.load(RASTGELE_ORMAN_DOSYASI),
        "lojistik_regresyon": joblib.load(LOJISTIK_DOSYASI),
    }


def _ikili_tahmin(model, veriler_olcekli):
    return int(model.predict(veriler_olcekli)[0])


def _olasilik_hesapla(model, veriler_olcekli):
    if hasattr(model, "predict_proba"):
        return float(model.predict_proba(veriler_olcekli)[0][1])
    return 0.0


MODELLER = None


def tahmin_hesapla(veriler):
    """
    Gelen 12 biomarker degerinden model bazli ve toplu tahmin uretir.
    veriler: [yas, anemi, kreatinin_fosfokinaz, ... , takip_suresi]
    """
    global MODELLER
    if MODELLER is None:
        MODELLER = _modelleri_yukle()
    veri_matrisi = np.array([veriler], dtype=float)
    olcekli_veri = MODELLER["olcekleyici"].transform(veri_matrisi)

    karar_agaci = _ikili_tahmin(MODELLER["karar_agaci"], olcekli_veri)
    knn = _ikili_tahmin(MODELLER["knn"], olcekli_veri)
    naive_bayes = _ikili_tahmin(MODELLER["naive_bayes"], olcekli_veri)
    rastgele_orman = _ikili_tahmin(MODELLER["rastgele_orman"], olcekli_veri)
    lojistik = _ikili_tahmin(MODELLER["lojistik_regresyon"], olcekli_veri)

    model_oylari = [karar_agaci, knn, naive_bayes, rastgele_orman, lojistik]
    toplu_tahmin = int(sum(model_oylari) >= 3)
    ortalama_olasilik = float(
        np.mean(
            [
                _olasilik_hesapla(MODELLER["karar_agaci"], olcekli_veri),
                _olasilik_hesapla(MODELLER["knn"], olcekli_veri),
                _olasilik_hesapla(MODELLER["naive_bayes"], olcekli_veri),
                _olasilik_hesapla(MODELLER["rastgele_orman"], olcekli_veri),
                _olasilik_hesapla(MODELLER["lojistik_regresyon"], olcekli_veri),
            ]
        )
    )

    return {
        "karar_agaci": karar_agaci,
        "knn": knn,
        "naive_bayes": naive_bayes,
        "rastgele_orman": rastgele_orman,
        "lojistik_regresyon": lojistik,
        "toplu_tahmin": toplu_tahmin,
        "olasilik": ortalama_olasilik,
    }
