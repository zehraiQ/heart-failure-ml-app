from django import forms

from .models import Doktor, Hasta, Randevu


def _girdi_sinifi():
    return (
        "form-kontrol w-full rounded-xl border border-slate-700/80 bg-slate-950/40 "
        "px-4 py-3 text-slate-100 shadow-inner transition duration-200 "
        "placeholder:text-slate-500 focus:border-cyan-500/50 focus:outline-none "
        "focus:ring-2 focus:ring-cyan-500/20"
    )


def _ikili_secenekler():
    return [("0", "Hayir"), ("1", "Evet")]


def _cinsiyet_secenekler():
    return [("1", "Erkek"), ("0", "Kadin")]


class TahminForm(forms.Form):
    """12 biomarker + hasta secimi; sunucu tarafinda min/max ve Turkce hata mesajlari."""

    hasta_id = forms.ModelChoiceField(
        queryset=Hasta.objects.none(),
        label="Hasta",
        empty_label="Hasta seciniz",
        widget=forms.Select(attrs={"class": _girdi_sinifi()}),
        error_messages={"invalid_choice": "Gecerli bir hasta seciniz.", "required": "Hasta secimi zorunludur."},
    )
    yas = forms.IntegerField(
        min_value=1,
        max_value=120,
        label="Yas",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "min": 1, "max": 120}),
        error_messages={
            "min_value": "Yas 1 ile 120 arasinda olmalidir.",
            "max_value": "Yas 1 ile 120 arasinda olmalidir.",
            "invalid": "Yas icin gecerli bir tam sayi giriniz.",
            "required": "Yas zorunludur.",
        },
    )
    anemi = forms.ChoiceField(
        choices=_ikili_secenekler(),
        label="Anemi",
        widget=forms.Select(attrs={"class": _girdi_sinifi()}),
        error_messages={"required": "Anemi alani zorunludur."},
    )
    kreatinin_fosfokinaz = forms.FloatField(
        min_value=0,
        max_value=8000,
        label="Kreatinin Fosfokinaz",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "step": "0.01", "min": 0, "max": 8000}),
        error_messages={
            "min_value": "Kreatinin fosfokinaz 0 ile 8000 arasinda olmalidir.",
            "max_value": "Kreatinin fosfokinaz 0 ile 8000 arasinda olmalidir.",
            "invalid": "Gecerli bir sayi giriniz.",
            "required": "Bu alan zorunludur.",
        },
    )
    diyabet = forms.ChoiceField(
        choices=_ikili_secenekler(),
        label="Diyabet",
        widget=forms.Select(attrs={"class": _girdi_sinifi()}),
        error_messages={"required": "Diyabet alani zorunludur."},
    )
    ejeksiyon_fraksiyonu = forms.FloatField(
        min_value=0,
        max_value=100,
        label="Ejeksiyon Fraksiyonu (%)",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "step": "0.01", "min": 0, "max": 100}),
        error_messages={
            "min_value": "Ejeksiyon fraksiyonu 0 ile 100 arasinda olmalidir.",
            "max_value": "Ejeksiyon fraksiyonu 0 ile 100 arasinda olmalidir.",
            "invalid": "Gecerli bir sayi giriniz.",
            "required": "Bu alan zorunludur.",
        },
    )
    yuksek_tansiyon = forms.ChoiceField(
        choices=_ikili_secenekler(),
        label="Yuksek Tansiyon",
        widget=forms.Select(attrs={"class": _girdi_sinifi()}),
        error_messages={"required": "Yuksek tansiyon alani zorunludur."},
    )
    trombosit = forms.FloatField(
        min_value=0,
        max_value=1000000,
        label="Trombosit",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "step": "0.01", "min": 0, "max": 1000000}),
        error_messages={
            "min_value": "Trombosit degeri negatif olamaz.",
            "max_value": "Trombosit degeri cok yuksek; 0 ile 1000000 arasinda olmalidir.",
            "invalid": "Gecerli bir sayi giriniz.",
            "required": "Bu alan zorunludur.",
        },
    )
    serum_kreatinin = forms.FloatField(
        min_value=0.1,
        max_value=15.0,
        label="Serum Kreatinin",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "step": "0.01", "min": 0.1, "max": 15}),
        error_messages={
            "min_value": "Serum kreatinin 0.1 ile 15 arasinda olmalidir.",
            "max_value": "Serum kreatinin 0.1 ile 15 arasinda olmalidir.",
            "invalid": "Gecerli bir sayi giriniz.",
            "required": "Bu alan zorunludur.",
        },
    )
    serum_sodyum = forms.FloatField(
        min_value=100,
        max_value=150,
        label="Serum Sodyum",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "step": "0.01", "min": 100, "max": 150}),
        error_messages={
            "min_value": "Serum sodyum 100 ile 150 arasinda olmalidir.",
            "max_value": "Serum sodyum 100 ile 150 arasinda olmalidir.",
            "invalid": "Gecerli bir sayi giriniz.",
            "required": "Bu alan zorunludur.",
        },
    )
    cinsiyet_erkek = forms.ChoiceField(
        choices=_cinsiyet_secenekler(),
        label="Cinsiyet",
        widget=forms.Select(attrs={"class": _girdi_sinifi()}),
        error_messages={"required": "Cinsiyet secimi zorunludur."},
    )
    sigara = forms.ChoiceField(
        choices=_ikili_secenekler(),
        label="Sigara",
        widget=forms.Select(attrs={"class": _girdi_sinifi()}),
        error_messages={"required": "Sigara alani zorunludur."},
    )
    takip_suresi = forms.IntegerField(
        min_value=0,
        max_value=500,
        label="Takip Suresi (gun)",
        widget=forms.NumberInput(attrs={"class": _girdi_sinifi(), "min": 0, "max": 500}),
        error_messages={
            "min_value": "Takip suresi 0 ile 500 gun arasinda olmalidir.",
            "max_value": "Takip suresi 0 ile 500 gun arasinda olmalidir.",
            "invalid": "Gecerli bir tam sayi giriniz.",
            "required": "Bu alan zorunludur.",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hasta_id"].queryset = Hasta.objects.all().order_by("ad_soyad")

    def temizlenmis_biyobelirtec_sozlugu(self):
        """Model ve tahmin fonksiyonu icin sozluk (float/bool)."""
        veri = self.cleaned_data
        hasta = veri["hasta_id"]

        def ikili_bool(alan):
            return bool(int(veri[alan]))

        return {
            "hasta": hasta,
            "yas": int(veri["yas"]),
            "anemi": ikili_bool("anemi"),
            "kreatinin_fosfokinaz": float(veri["kreatinin_fosfokinaz"]),
            "diyabet": ikili_bool("diyabet"),
            "ejeksiyon_fraksiyonu": float(veri["ejeksiyon_fraksiyonu"]),
            "yuksek_tansiyon": ikili_bool("yuksek_tansiyon"),
            "trombosit": float(veri["trombosit"]),
            "serum_kreatinin": float(veri["serum_kreatinin"]),
            "serum_sodyum": float(veri["serum_sodyum"]),
            "cinsiyet_erkek": ikili_bool("cinsiyet_erkek"),
            "sigara": ikili_bool("sigara"),
            "takip_suresi": int(veri["takip_suresi"]),
        }

    def tahmin_vektoru(self):
        """ai_entegrasyon.tahmin_hesapla icin 12 elemanli liste (sirali)."""
        s = self.temizlenmis_biyobelirtec_sozlugu()
        return [
            float(s["yas"]),
            float(s["anemi"]),
            s["kreatinin_fosfokinaz"],
            float(s["diyabet"]),
            s["ejeksiyon_fraksiyonu"],
            float(s["yuksek_tansiyon"]),
            s["trombosit"],
            s["serum_kreatinin"],
            s["serum_sodyum"],
            float(s["cinsiyet_erkek"]),
            float(s["sigara"]),
            float(s["takip_suresi"]),
        ]


class HastaForm(forms.ModelForm):
    class Meta:
        model = Hasta
        fields = ["ad_soyad", "tc_kimlik_no", "dogum_tarihi", "cinsiyet", "telefon"]
        widgets = {
            "ad_soyad": forms.TextInput(attrs={"class": _girdi_sinifi()}),
            "tc_kimlik_no": forms.TextInput(attrs={"class": _girdi_sinifi(), "maxlength": 11}),
            "dogum_tarihi": forms.DateInput(attrs={"type": "date", "class": _girdi_sinifi()}),
            "cinsiyet": forms.Select(attrs={"class": _girdi_sinifi()}, choices=_cinsiyet_secenekler()),
            "telefon": forms.TextInput(attrs={"class": _girdi_sinifi()}),
        }

    def clean_tc_kimlik_no(self):
        tc = self.cleaned_data["tc_kimlik_no"].strip()
        if not tc.isdigit() or len(tc) != 11:
            raise forms.ValidationError("TC Kimlik No 11 haneli sayisal olmalidir.")
        return tc


class DoktorForm(forms.ModelForm):
    class Meta:
        model = Doktor
        fields = ["ad_soyad", "uzmanlik_alani", "eposta", "telefon", "aktif_mi"]
        widgets = {
            "ad_soyad": forms.TextInput(attrs={"class": _girdi_sinifi()}),
            "uzmanlik_alani": forms.TextInput(attrs={"class": _girdi_sinifi()}),
            "eposta": forms.EmailInput(attrs={"class": _girdi_sinifi()}),
            "telefon": forms.TextInput(attrs={"class": _girdi_sinifi()}),
            "aktif_mi": forms.CheckboxInput(attrs={"class": "rounded border-slate-600 text-cyan-500"}),
        }


class RandevuForm(forms.ModelForm):
    class Meta:
        model = Randevu
        fields = ["hasta", "doktor", "randevu_tarihi", "notlar", "durum"]
        widgets = {
            "hasta": forms.Select(attrs={"class": _girdi_sinifi()}),
            "doktor": forms.Select(attrs={"class": _girdi_sinifi()}),
            "randevu_tarihi": forms.DateTimeInput(attrs={"type": "datetime-local", "class": _girdi_sinifi()}),
            "notlar": forms.Textarea(attrs={"rows": 3, "class": _girdi_sinifi()}),
            "durum": forms.Select(attrs={"class": _girdi_sinifi()}),
        }
