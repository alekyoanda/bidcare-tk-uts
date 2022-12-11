from django.urls import path
from general_user import views

app_name = "general_user"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_user, name="login"),
    path('login_flutter/', views.login_user_flutter, name="login_flutter"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('get_galang/<id>', views.get_galang, name="get_galang"),
    path('get_lelang/<id>', views.get_lelang, name="get_lelang"),
    path('get_galang/json/', views.show_json_galang, name="show_json_galang"),
    path('get_lelang/json/', views.show_json_lelang, name="show_json_lelang"),

]
