
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect,  JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core import serializers
from general_user.forms import RegisterForm, RekeningBankForm
from general_user.models import GeneralUser
from resipien.models import GalangDana
# from lelang.models import BarangLelang
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
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('general_user:homepage'))
        else:
            messages.info(request, 'Email atau password tidak valid.')

    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "general_user/login.html", context)

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

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('general_user:homepage'))

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
    data = BarangLelang.objects.filter(pelelang=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# @login_required(login_url='/todolist/login')
def show_json_galang(request):
    data = GalangDana.objects.all()
    print(data)
    # data = GalangDana.objects.filter(user=GeneralUser.objects.get(user=request.user))
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")