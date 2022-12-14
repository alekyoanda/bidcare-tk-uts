from django.utils import timezone
from general_user.models import GeneralUser, RekeningBank
from lelang.models import *
from resipien.models import GalangDana
from django import forms
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class BarangLelangForm(forms.ModelForm):
    error_messages = {
        'rekening_mismatch': ("Nomor rekening tidak valid."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kategori_barang'].widget.attrs.update({'class': 'select form-select'})
        self.fields['gambar'].required = False
        
    class Meta:
        model = BarangLelang
        fields = ['nama_barang', 'deskripsi', 'gambar', 'starting_bid', 'tanggal_berakhir', 'kategori_barang']
        widgets = {
            'tanggal_berakhir': DateInput(),
        }

    def clean_tanggal_berakhir(self):
        tanggal_berakhir = self.cleaned_data.get("tanggal_berakhir")
        if (tanggal_berakhir <= timezone.now()):
            raise forms.ValidationError("End date should be greater than start date.")
        return tanggal_berakhir
    

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['banyak_bid']

class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ['teks']