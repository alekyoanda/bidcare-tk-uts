from datetime import date, datetime
import json
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.timesince import timesince
from general_user.models import GeneralUser
from lelang.forms import BarangLelangForm, BiddingForm, KomentarForm
from lelang.models import BarangLelang, Bid, Komentar
from resipien.models import GalangDana
from django.contrib.auth.decorators import login_required
from django.core import serializers

# Create your views here.
def index(request):
    daftar_kategori = {x[1] for x in BarangLelang.KATEGORI_CHOICES}
    context = {
        "daftar_kategori": daftar_kategori,
    }
    return render(request, "lelang/show_barang_lelang.html", context)

def index_by_kategori(request, nama_kategori):
    daftar_kategori = {x[1] for x in BarangLelang.KATEGORI_CHOICES}
    context = {
        "daftar_kategori": daftar_kategori,
    }
    return render(request, "lelang/show_barang_lelang.html", context)

def get_json_lelang(request):
    daftar_barang_lelang = BarangLelang.objects.all().order_by('-status_keaktifan', 'tanggal_berakhir')
    for barang_lelang in daftar_barang_lelang:
        if timesince(barang_lelang.tanggal_berakhir)[0] != "0":
            barang_lelang.status_keaktifan = False
            barang_lelang.save()
    response = json.loads(serializers.serialize('json', daftar_barang_lelang))
    return JsonResponse(response, safe=False)

def get_json_lelang_by_kategori(request, nama_kategori):
    kategori = [x for (x, y) in BarangLelang.KATEGORI_CHOICES if y == nama_kategori][0]
    daftar_barang_lelang = BarangLelang.objects.filter(kategori_barang=kategori).order_by('-status_keaktifan', 'tanggal_berakhir')
    for barang_lelang in daftar_barang_lelang:
        if timesince(barang_lelang.tanggal_berakhir)[0] != "0":
            barang_lelang.status_keaktifan = False
            barang_lelang.save()
    response = json.loads(serializers.serialize('json', daftar_barang_lelang))
    return JsonResponse(response, safe=False)

@login_required(login_url='/login')
def create_lelang(request, galang_dana_id):
    galang_dana_tujuan = GalangDana.objects.get(pk=galang_dana_id)
    form = BarangLelangForm()
    if (request.method == "POST"):
        form = BarangLelangForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.galang_dana_tujuan = GalangDana.objects.get(pk=int(galang_dana_id))
            item.pelelang = GeneralUser.objects.get(user=request.user)
            item.bid_tertinggi = item.starting_bid
            item.save()

            return HttpResponseRedirect(reverse("lelang:rincian_lelang", args=[item.pk]))
    
    context = {
        "galang_dana": galang_dana_tujuan,
        "form": form
    }
    return render(request, "lelang/create_lelang.html", context)

def rincian_lelang(request, lelang_id):
    barang_lelang = BarangLelang.objects.get(pk=int(lelang_id))
    form = BiddingForm()
    form_komentar = KomentarForm()
    bids = Bid.objects.filter(barang_lelang=lelang_id).order_by('-banyak_bid')
    bid_tertinggi = bids.first()
    semua_komentar = Komentar.objects.filter(barang_lelang=lelang_id)
    
    bid_diberikan = 0.7 * barang_lelang.bid_tertinggi
    rasio_donasi = (bid_diberikan / barang_lelang.galang_dana_tujuan.target) * 100

    context = {
        "form": form,
        "form_komentar": form_komentar,
        "item": barang_lelang,
        "bids": bids,
        "bid_tertinggi": bid_tertinggi,
        "semua_komentar": semua_komentar,
        "rasio_donasi": rasio_donasi,
        "bid_diberikan": bid_diberikan
    }
    return render(request, "lelang/rincian_lelang.html", context)

def get_rincian_lelang_json(request, id):
    barang_lelang = BarangLelang.objects.get(pk=id)
    penggalang_dana = barang_lelang.galang_dana_tujuan
    
    
    return JsonResponse()

@login_required(login_url='/login')
def bid_barang_lelang(request, lelang_id):
    if request.method == "POST":
        form = BiddingForm(request.POST)
        barang_lelang = BarangLelang.objects.get(pk=lelang_id)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = GeneralUser.objects.get(user=request.user)
            bid.barang_lelang = barang_lelang
            if bid.banyak_bid > barang_lelang.bid_tertinggi:
                barang_lelang.bid_tertinggi = bid.banyak_bid
                barang_lelang.save()
                bid.save()
                response = json.loads(serializers.serialize('json', [bid]))
                response[0]["username"] = bid.user.user.username

                return JsonResponse(response, safe=False)
    
        return HttpResponseBadRequest(barang_lelang.bid_tertinggi)
        
@login_required(login_url='/login')
def komentar_barang_lelang(request, lelang_id):
    if request.method == "POST":
        form = KomentarForm(request.POST)
        if form.is_valid():
            komentar = form.save(commit=False)
            komentar.user = GeneralUser.objects.get(user=request.user)
            komentar.barang_lelang = BarangLelang.objects.get(pk=lelang_id)
            komentar.save()
            response = json.loads(serializers.serialize('json', [komentar]))
            response[0]["username"] = komentar.user.user.username

            return JsonResponse(response, safe=False)
    
        return HttpResponseBadRequest()
