from django.urls import path
from resipien import views
from resipien.views import show_buat_galang, show_daftar_galang, show_detail_galang, show_json_galang, show_json_komentar, show_json_lelang, show_json_bank, show_json_akun, flutter_buat_galang, flutter_tambah_komentar


app_name = "resipien"

urlpatterns = [
    path('', show_daftar_galang, name="homepage"),
    path('buat/', show_buat_galang, name='buat'),
    path('daftar/', show_daftar_galang, name='daftar'),
    path('detail/<int:id>/', show_detail_galang, name='detail'),
    path('json', show_json_galang, name='json-galang'),
    path('komentarjson/<int:id>/', show_json_komentar, name='json-komen'),
    path('lelangjson/<int:id>/', show_json_lelang, name='json-lelang'),
    path('bankjson/<int:id>/', show_json_bank, name='json-bank'),
    path('akunjson/<int:id>/', show_json_akun, name='json-akun'),
    path("fbuatGalang/", flutter_buat_galang, name="flutter-buat"),
    path("ftambahKomentar/<int:id>/", flutter_tambah_komentar, name="flutter-komen"),
]
