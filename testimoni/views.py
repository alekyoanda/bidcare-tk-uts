import random
from testimoni.models import TestimoniList
from testimoni.forms import TestimoniForm

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# Method untuk menampilkan testimoni dari semua pengguna
def show_testimoni(request) :   
    # Menampilkan semua testimoni (maupun bagi yang belum login)
    list_testimoni = TestimoniList.objects.all()

    # Mengambil 3 testimoni secara acak untuk ditambahkan ke carousel
    initiate_list_testimoni = list(TestimoniList.objects.all()) 
    random_testimoni = random.sample(initiate_list_testimoni, 3)
    first_random_testimoni = random_testimoni[0]
    second_random_testimoni = random_testimoni[1]
    third_random_testimoni = random_testimoni[2]

    # Membuat tampilan form
    testimoni_form = TestimoniForm(request.POST)

    context = {
        'list_testimoni' : list_testimoni,
        'testimoni_form' : testimoni_form,
        'first_random_testimoni' : first_random_testimoni,
        'second_random_testimoni' : second_random_testimoni,
        'third_random_testimoni' : third_random_testimoni
    }

    return render(request, "testimoni.html", context)

# Method untuk menampilkan data testimoni dengan format json
def show_testimoni_json(request):
    list_testimoni = TestimoniList.objects.all()
    return HttpResponse(serializers.serialize('json', list_testimoni), content_type="application/json")

# Method untuk menampilkan data acak testimoni dengan format json
def show_random_testimoni(request):
    list_testimoni = list(TestimoniList.objects.all())
    random_testimoni = random.sample(list_testimoni, 3)
    
    return HttpResponse(serializers.serialize('json', random_testimoni), content_type="application/json")

# Method untuk menambahkan testimoni (dibutuhkan login akun)
@login_required(login_url='/login')
def add_testimoni(request) :

    nama = request.POST.get("nama")
    title = request.POST.get("title")
    target = request.POST.get("target")
    pesan = request.POST.get("pesan")

    if len(nama) == 0 :
        nama = "Anonymous"
        
    if len(target) == 0 :
        target = "-"

    testimoni_baru = TestimoniList(nama=nama, title=title, target=target, pesan=pesan)
    testimoni_baru.save()

    return HttpResponse(status=200)