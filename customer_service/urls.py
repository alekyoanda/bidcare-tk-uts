from django.urls import path
from customer_service import views

app_name = "customer_service"

urlpatterns = [
    path('', views.show_faq, name="show_faq"),
    path('nanya-flutter/', views.nanya_flutter, name="nanya_flutter"),
    path('jawab-flutter/<int:id>', views.jawab_flutter, name="jawab_flutter"),
    path('delete-flutter/<int:id>', views.delete_flutter, name="delete_flutter"),
    path('add-pertanyaan/', views.add_pertanyaan, name="add_pertanyaan"),
    path('pertanyaan-masuk/', views.pertanyaan_masuk, name="pertanyaan_masuk"),
    path('pertanyaan-masuk/add-jawaban/<int:id>', views.add_jawaban, name="add_jawaban"),
    path('pertanyaan-masuk/delete/<int:id>', views.deletePertanyaan, name="delete"),
    path('pertanyaan-masuk/json/pertanyaan', views.jsonPertanyaan, name="jsonPertanyaan"),
    path('pertanyaan-masuk/json/faq', views.jsonFAQ, name="jsonFAQ"),
    path('json/pertanyaan', views.jsonPertanyaan, name="jsonPertanyaan"),
    path('json/faq', views.jsonFAQ, name="jsonFAQ"),
]
