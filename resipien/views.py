
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from general_user.forms import RekeningBankForm
from general_user.models import GeneralUser, RekeningBank
from resipien.models import GalangDana, KomentarGalang
from resipien.forms import GalangForm, KomentarGalangForm
import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.utils.timesince import timesince
from lelang.models import BarangLelang
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url='/general_user/login/')
@csrf_protect
def show_buat_galang(request):
    formGalang = GalangForm()
    formBank = RekeningBankForm()
    if request.method == 'POST':
        formGalang = GalangForm(request.POST, request.FILES)
        formBank = RekeningBankForm(request.POST)
        if formGalang.is_valid() & formBank.is_valid():
            user = GeneralUser.objects.get(user=request.user)
            tujuan = formGalang.cleaned_data["tujuan"]
            judul = formGalang.cleaned_data["judul"]
            deskripsi = formGalang.cleaned_data["deskripsi"]
            target = formGalang.cleaned_data["target"]
            gambar = formGalang.cleaned_data["gambar"]
            tanggal_pembuatan = datetime.datetime.now()
            tanggal_berakhir = formGalang.cleaned_data["tanggal_berakhir"]
            terkumpul = 0
            status_keaktifan = True
            akun_bank = formBank.save()
            GalangDana.objects.create(user=user, akun_bank=akun_bank, tujuan=tujuan, judul=judul, deskripsi=deskripsi, target=target, gambar=gambar, tanggal_pembuatan=tanggal_pembuatan, tanggal_berakhir=tanggal_berakhir, status_keaktifan=status_keaktifan, terkumpul=terkumpul)
            return redirect('resipien:daftar')
        else:
            formGalang = GalangForm()
            formBank = RekeningBankForm()
    return render(request, "resipien/buat-galang.html", {'formGalang':formGalang, 'formBank':formBank})


def show_daftar_galang(request):     
    data_galang = GalangDana.objects.all().order_by('-status_keaktifan')
    for galang in data_galang:
        if timesince(galang.tanggal_berakhir)[0] != "0" or galang.terkumpul == galang.target:
            galang.status_keaktifan = False
            galang.save()
    content = {
        'data_galang': data_galang,
    }
    return render(request, "resipien/galang-dana.html", content)

def show_detail_galang(request, id):     
    objek_galang = GalangDana.objects.get(id=id)
    data_komentar = KomentarGalang.objects.filter(objek_galang=id)
    objek_lelang = BarangLelang.objects.filter(galang_dana_tujuan = objek_galang).order_by('-status_keaktifan', 'tanggal_berakhir')
    formKomentar = KomentarGalangForm(request.POST or None)
    rasio_donasi = objek_galang.terkumpul/objek_galang.target * 100
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False
    if request.method == "POST" and is_ajax:
        user = GeneralUser.objects.get(user=request.user)
        username = request.user.get_username()        
        objek_galang = GalangDana.objects.get(id=id)
        komentar = request.POST.get('komen')
        tanggal_komentar = datetime.datetime.now()
        KomentarGalang.objects.create(user=user, username=username, objek_galang=objek_galang, komentar=komentar, tanggal_komentar=tanggal_komentar)
        return JsonResponse({"Message": 'Your new task has been added!'},status=200)
    if request.method == "GET" and is_ajax:
        data_komentar = KomentarGalang.objects.filter(objek_galang = GalangDana.objects.get(id=id)).order_by('tanggal_komentar')[::-1]
        return HttpResponse(serializers.serialize('json',data_komentar), content_type="application/json")
    context = {
        "galang": objek_galang,
        "data_komentar": data_komentar,
        "formKomentar": formKomentar,
        "data_lelang" : objek_lelang,
        "rasio_donasi" : rasio_donasi
    }
    return render(request, "resipien/detail-galang.html",  context)

def show_json_galang(request):
    data_galang = GalangDana.objects.all().order_by('-status_keaktifan')
    return HttpResponse(serializers.serialize("json", data_galang), content_type="application/json")

def show_json_bank(request, id):
    akun_bank = RekeningBank.objects.filter(pk = id)
    return HttpResponse(serializers.serialize("json", akun_bank), content_type="application/json")  

def show_json_komentar(request, id):
    data_komentar = KomentarGalang.objects.filter(objek_galang=id)
    return HttpResponse(serializers.serialize("json", data_komentar), content_type="application/json")  

def show_json_lelang(request, id):
    objek_galang = GalangDana.objects.get(id=id)
    objek_lelang = BarangLelang.objects.filter(galang_dana_tujuan = objek_galang).order_by('-status_keaktifan', 'tanggal_berakhir')
    return HttpResponse(serializers.serialize("json", objek_lelang), content_type="application/json")  

def show_json_akun(request, id):
    objek_user = GeneralUser.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", objek_user), content_type="application/json")  

# Flutter
@csrf_exempt
def flutter_buat_galang(request):
    if request.method == "POST":
        user = GeneralUser.objects.get(user=request.user)
        tujuan = request.POST.get("tujuan")
        judul = request.POST.get("judul")
        deskripsi = request.POST.get("deskripsi")
        target = request.POST.get("target")
        tanggal_pembuatan = datetime.datetime.now()
        tanggal_berakhir = request.POST.get("tanggal_berakhir")
        terkumpul = 0
        status_keaktifan = True
        nama_pemilik = request.POST.get("nama_pemilik")
        nama_bank = request.POST.get("nama_bank")
        no_rekening = request.POST.get("no_rekening")
        akun_bank = RekeningBank.objects.create(nama_pemilik = nama_pemilik, nama_bank = nama_bank, no_rekening = no_rekening)
        GalangDana.objects.create(user=user, akun_bank=akun_bank, tujuan=tujuan, judul=judul, deskripsi=deskripsi, target=target, tanggal_pembuatan=tanggal_pembuatan, tanggal_berakhir=tanggal_berakhir, status_keaktifan=status_keaktifan, terkumpul=terkumpul)

        return HttpResponse(b"CREATED", status=201)
            
    return HttpResponseNotFound()

@csrf_exempt
def flutter_tambah_komentar(request, id):
    if request.method == "POST":
        user = GeneralUser.objects.get(user=request.user)
        username = request.user.get_username()        
        objek_galang = GalangDana.objects.get(id=id)
        komentar = request.POST.get('komentar')
        tanggal_komentar = datetime.datetime.now()
        KomentarGalang.objects.create(user=user, username=username, objek_galang=objek_galang, komentar=komentar, tanggal_komentar=tanggal_komentar)

        return HttpResponse(b"CREATED", status=201)
            
    return HttpResponseNotFound()

