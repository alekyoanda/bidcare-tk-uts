from django.urls import path
from lelang import views
from django.conf import settings


app_name = "lelang"

urlpatterns = [
    path('', views.index, name="show_barang_lelang"),
    path('get_json_lelang', views.get_json_lelang, name="get_json_lelang"),
    path('create_lelang/<int:galang_dana_id>', views.create_lelang, name="create_lelang"),
    path('<int:lelang_id>', views.rincian_lelang, name="rincian_lelang"),
    path('bid_barang_lelang/<int:lelang_id>', views.bid_barang_lelang, name="bid_barang_lelang"),
    path('komentar_barang_lelang/<int:lelang_id>', views.komentar_barang_lelang, name="komentar_barang_lelang"),
    path('json', views.get_json_lelang, name="get_json_lelang"),
    path('json/<int:id>', views.get_rincian_lelang_json, name="get_rincian_json_lelang"),
    # path('kategori/<str:nama_kategori>/json', views.get_json_lelang_by_kategori, name="get_json_lelang_by_kateori"),
    # path('kategori/<str:nama_kategori>', views.index_by_kategori, name="show_lelang_by_kategori")
]

