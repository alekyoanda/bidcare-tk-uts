# from lib2to3.pgen2.token import GREATER
from inspect import stack
import json
import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from general_user.forms import RekeningBankForm
from general_user.models import GeneralUser
from resipien.models import GalangDana, KomentarGalang
from resipien.forms import GalangForm, KomentarGalangForm
import datetime
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.utils.timesince import timesince

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
    formKomentar = KomentarGalangForm(request.POST or None)
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
    }
    if request.user.is_authenticated:
        data_galang_user = GalangDana.objects.filter(user=GeneralUser.objects.get(user=request.user))
        context = {
        "galang": objek_galang,
        "data_komentar": data_komentar,
        "formKomentar": formKomentar,
        "data_galang_user":data_galang_user
        }
        return render(request, "resipien/detail-galang.html",  context)
    return render(request, "resipien/detail-galang.html",  context)

def show_json(request):
    data_galang = GalangDana.objects.all()
    return HttpResponse(serializers.serialize('json',data_galang), content_type="application/json")


@login_required(login_url='/general_user/login/')
def delete_galang(request, id):
    objek_galang = GalangDana.objects.get(id = id)
    objek_galang.delete()



