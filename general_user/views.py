
import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect,  JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core import serializers
from general_user.forms import RegisterForm, RekeningBankForm
from general_user.models import GeneralUser, RekeningBank
from resipien.models import GalangDana
from lelang.models import BarangLelang
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# Create your views here.

def homepage(request):
    # data_lelang = BarangLelang.objects.filter(pelelang=request.user)
    # data_galang = GalangDana.objects.filter(user=request.user)
    # context = {
    #     'data_lelang':data_lelang,
    #     'data_galang':data_galang
    # }
    return render(request, "general_user/home.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response =  HttpResponseRedirect(reverse('general_user:homepage'))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Email atau password tidak valid.')

    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "general_user/login.html", context)

@csrf_exempt
def login_user_flutter(request):
    if request.method == 'POST':
        print('masuk ke post login')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            return JsonResponse({
                "status": True,
                "message": "Successfully Logged In!",
                # Insert any extra data if you want to pass data to Flutter
                }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Login, check your email/password."
            }, status=401)

def register(request):
    form = RegisterForm()
    form_bank = RekeningBankForm()
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form_bank = RekeningBankForm(request.POST)
        if form.is_valid() and form_bank.is_valid():
            user = form.save()
            rekening_bank = form_bank.save()
            GeneralUser.objects.create(user=user, akun_bank=rekening_bank, no_ponsel=form.cleaned_data.get('no_ponsel'))
            
            login(request, user)

            return redirect('general_user:homepage')
        else:
            print(form_bank.errors)
            
    context = {"form": form, "form_bank": form_bank}
    return render(request, "general_user/register.html", context)

@csrf_exempt
def register_flutter(request):
    # is_user_already_exist = User.objects.filter(username="cobacobacoba")
    # print(is_user_already_exist.exists())
    # return  HttpResponse(serializers.serialize("json", is_user_already_exist), content_type="application/json")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('first_name')
        nomor_ponsel = request.POST.get('nomor_ponsel')
        nama_bank = request.POST.get('nama_bank')
        no_rekening = request.POST.get('no_rekening')
        nama_pemilik = request.POST.get('nama_pemilik')
        is_user_already_exist = User.objects.filter(username=username).exists()
        # return  HttpResponse(serializers.serialize("json", is_user_already_exist), content_type="application/json")
        print(username)
        print(is_user_already_exist)
        if (first_name == '') or (last_name == '') or (email =='') or (username == '') or (password == '') or (nomor_ponsel == '') or (no_rekening == '') or (nama_pemilik == ''): 
            return JsonResponse({
              "status": False,
              "message": "Harap mengisi semua form :)"
            }, status=401)
        elif (len(nomor_ponsel)>16 or not nomor_ponsel.isnumeric()):
            return JsonResponse({
              "status": False,
              "message": "Nomor Ponsel yang dimasukkan tidak sesuai :)"
            }, status=401)
        elif (len(no_rekening)>16 or not no_rekening.isnumeric()):
            return JsonResponse({
              "status": False,
              "message": "Password harus sama"
            }, status=401)
        elif (not is_user_already_exist):
            user = User.objects.create_user(username=username,password=password)
            user.save()
            rekening_bank = RekeningBank.objects.create(nama_pemilik = nama_pemilik, nama_bank = nama_bank, no_rekening = no_rekening)
            rekening_bank.save()
            GeneralUser.objects.create(user=user, akun_bank=rekening_bank, no_ponsel = nomor_ponsel)
            user = authenticate(request, username=username, password=password)
            return JsonResponse({
                "status": True,
                "username": user.username,
            }, status=200)
        else:
            return JsonResponse({
              "status": False,
              "message": "Username sudah terdaftar"
            }, status=401)
    else:
        return JsonResponse({
            "status": "Something Wrong T_T"
        }, status=401)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('general_user:homepage'))
    response.delete_cookie('last_login')
    return response

def get_galang(request, id):
    if request.method == "GET":
        galang = get_object_or_404(GalangDana, id = id)
    
    result = {
        'fields':{
            'judul': galang.judul,
            'gambar': galang.gambar,
            'deskripsi': galang.deskripsi,
            'tujuan': galang.tujuan,
            'tanggal_pembuatan': galang.tanggal_pembuatan,
            'tanggal_berakhir': galang.tanggal_berakhir,
            'terkumpul': galang.terkumpul,
            'target': galang.target,
            'status_keaktifan': galang.status_keaktifan,
            },
            'pk': galang.pk
        }
        
    return JsonResponse(result)

def get_lelang(request, id):
    if request.method == "GET":
        lelang = get_object_or_404(BarangLelang, id = id)
    
    result = {
        'fields':{
            'nama_barang': lelang.nama_barang,
            'gambar': lelang.gambar,
            'deskripsi': lelang.deskripsi,
            'starting_bid': lelang.starting_bid,
            'tanggal_mulai': lelang.tanggal_mulai,
            'tanggal_berakhir': lelang.tanggal_berakhir,
            'bid_tertinggi': lelang.bid_tertinggi,
            'kategori_barang': lelang.kategori_barang,
            'status_keaktifan': lelang.status_keaktifan,
            },
            'pk': lelang.pk
        }
        
    return JsonResponse(result)

# @login_required(login_url='/todolist/login')
def show_json_lelang(request):
    data = BarangLelang.objects.filter(pelelang=GeneralUser.objects.get(user=request.user))
    # data = BarangLelang.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# @login_required(login_url='/todolist/login')
def show_json_galang(request):
    # data = GalangDana.objects.filter(user=GeneralUser.objects.get(user=request.user))
    data = GalangDana.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_nama(request):
    return JsonResponse({
                "nama": request.user.username,
            }, status=200)