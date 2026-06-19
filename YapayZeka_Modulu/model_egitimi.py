from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


MODEL_DIZINI = Path(__file__).resolve().parent
PROJE_KOK = MODEL_DIZINI.parent
VERI_DOSYASI_ADI = "heart_failure_clinical_records_dataset.csv"

HEDEF_ALAN = "DEATH_EVENT"
OZELLIK_ALANLARI = [
    "age",
    "anaemia",
    "creatinine_phosphokinase",
    "diabetes",
    "ejection_fraction",
    "high_blood_pressure",
    "platelets",
    "serum_creatinine",
    "serum_sodium",
    "sex",
    "smoking",
    "time",
]


def veriyi_yukle():
    # Veri dosyasini tek bir noktada yukleyerek tekrarli kodu engeller.
    olasi_dosyalar = [
        PROJE_KOK / VERI_DOSYASI_ADI,
        MODEL_DIZINI / VERI_DOSYASI_ADI,
    ]
    veri_dosyasi = next((dosya for dosya in olasi_dosyalar if dosya.exists()), None)
    if veri_dosyasi is None:
        raise FileNotFoundError(
            f"Veri dosyasi bulunamadi. Beklenen konumlar: {olasi_dosyalar}"
        )

    veri = pd.read_csv(veri_dosyasi)
    return veri[OZELLIK_ALANLARI], veri[HEDEF_ALAN]


def modelleri_hazirla():
    return {
        "karar_agaci.pkl": DecisionTreeClassifier(random_state=42),
        "knn.pkl": KNeighborsClassifier(n_neighbors=7),
        "naive_bayes.pkl": GaussianNB(),
        "rastgele_orman.pkl": RandomForestClassifier(
            n_estimators=200, random_state=42, class_weight="balanced"
        ),
        "lojistik_regresyon.pkl": LogisticRegression(max_iter=1000, random_state=42),
    }


def model_egit_ve_kaydet():
    ozellikler, etiketler = veriyi_yukle()
    x_egitim, _, y_egitim, _ = train_test_split(
        ozellikler,
        etiketler,
        test_size=0.20,
        random_state=42,
        stratify=etiketler,
    )

    olcekleyici = StandardScaler()
    x_egitim_olcekli = olcekleyici.fit_transform(x_egitim)
    joblib.dump(olcekleyici, MODEL_DIZINI / "olcekleyici.pkl")

    for dosya_adi, model in modelleri_hazirla().items():
        model.fit(x_egitim_olcekli, y_egitim)
        joblib.dump(model, MODEL_DIZINI / dosya_adi)
        print(f"Kaydedildi: {dosya_adi}")

    print("Tum modeller basariyla egitildi ve kaydedildi.")


if __name__ == "__main__":
    model_egit_ve_kaydet()
