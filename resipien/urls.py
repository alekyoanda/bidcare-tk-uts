from django.urls import path
from resipien import views
from resipien.views import show_buat_galang, show_daftar_galang, show_detail_galang, show_json_galang, show_json_detail, show_json_komentar


app_name = "resipien"

urlpatterns = [
    path('', show_daftar_galang, name="homepage"),
    path('buat/', show_buat_galang, name='buat'),
    path('daftar/', show_daftar_galang, name='daftar'),
    path('detail/<int:id>/', show_detail_galang, name='detail'),
    path('json', show_json_galang, name='json-galang'),
    path('detailjson/<int:id>/', show_json_detail, name='json-detail'),
    path('komentarjson/<int:id>/', show_json_komentar, name='json-komen'),
]