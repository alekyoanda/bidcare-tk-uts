from django.urls import path
from testimoni import views

app_name = "testimoni"

urlpatterns = [
    path('', views.show_testimoni, name="show_testimoni"),
    path('json/', views.show_testimoni_json, name="show_testimoni_json"),
    path('json-random/', views.show_random_testimoni, name="show_random_testimoni"),
    path('add-testimoni/', views.add_testimoni, name="add_testimoni"),
    path('add-testimoni-flutter/', views.add_testimoni_flutter, name="add_testimoni_flutter")
]