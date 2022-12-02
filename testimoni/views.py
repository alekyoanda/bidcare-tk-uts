import json
import random
from testimoni.models import TestimoniList
from testimoni.forms import TestimoniForm

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators.csrf import csrf_exempt

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
    if request.method == "POST" :
        
        # Mengambil data dari form (kecuali user)
        user_logged_in = request.user
        nama = request.POST.get("nama")
        target = request.POST.get("target")
        pesan = request.POST.get("pesan")

        # Isi form default jika nama dan target tidak diisi
        if len(nama) == 0 :
            nama = "Anonymous"
            
        if len(target) == 0 :
            target = "-"

        # Membuat objek testimoni baru dan save
        testimoni_baru = TestimoniList(user=user_logged_in, nama=nama, target=target, pesan=pesan)
        testimoni_baru.save()

    return HttpResponse(status=200)

@csrf_exempt
def add_testimoni_flutter(request):
    data = request.body.decode('utf-8')
    new_data = json.loads(data)
    new_testimoni = TestimoniList(**new_data)
    new_testimoni.save()

    return HttpResponse(status=200)