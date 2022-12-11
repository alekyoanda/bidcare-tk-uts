from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customer_service.forms import JawabanForm, PertanyaanForm
from django.core import serializers 
from customer_service.models import FAQ, Pertanyaan
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def index(request):
    return HttpResponse("Ini halaman customer service")

def show_faq(request):
    # list_faq = FAQ.objects.filter(is_answered=True)

    form_jawaban = JawabanForm(request.POST)
    form_pertanyaan = PertanyaanForm(request.POST)
    list_faq = FAQ.objects.all()
    list_pertanyaan = Pertanyaan.objects.filter(is_answered=False)

    context = { 
        "form_jawaban" : form_jawaban,
        'form_pertanyaan': form_pertanyaan,
        "list_faq" : list_faq,
        "list_pertanyaan" : list_pertanyaan
    }

    return render(request, "faq.html", context)

@staff_member_required
def pertanyaan_masuk(request):
    form_jawaban = JawabanForm(request.POST)
    list_pertanyaan = Pertanyaan.objects.filter(is_answered=False)

    context = { 
        "form_jawaban" : form_jawaban,
        "list_pertanyaan" : list_pertanyaan
    }
    
    return render(request, "pertanyaan_masuk.html", context)

@csrf_exempt
def nanya_flutter(request):
    if request.method == "POST":
        kategori = request.POST.get('kategori')
        teks_pertanyaan = request.POST.get('teks_pertanyaan')
        new_pertanyaan = Pertanyaan(kategori=kategori, teks_pertanyaan=teks_pertanyaan)
        new_pertanyaan.save()

        res = { "model": "customer_service.pertanyaan", 
                "pk": new_pertanyaan.pk, 
                "fields": { "kategori": new_pertanyaan.kategori, 
                            "teks_pertanyaan": new_pertanyaan.teks_pertanyaan, 
                            "is_answered": new_pertanyaan.is_answered } }
    
        return HttpResponse(b"CREATED", status=201)
            
    return HttpResponseNotFound()
    
# @staff_member_required
# def jawab(request,id):
#     form_jawaban = JawabanForm(request.POST)
#     pertanyaan = Pertanyaan.objects.get(id=id)

#     context = { 
#         "form_jawaban" : form_jawaban,
#         "pertanyaan" : pertanyaan,
#         "pk" : id
#     }
    
#     return render(request, "jawab.html", context)

# @staff_member_required
# def jawab(request,id):
#     form_jawaban = JawabanForm(request.POST)
#     pertanyaan = Pertanyaan.objects.get(id=id)

#     context = { 
#         "form_jawaban" : form_jawaban,
#         "pertanyaan" : pertanyaan,
#         "pk" : id
#     }
    
#     return render(request, "jawab.html", context)

@csrf_exempt
def deletePertanyaan(request,id):
    pertanyaan_del = Pertanyaan.objects.get(id=id)
    pertanyaan_del.delete()

    return HttpResponse()

@staff_member_required 
def add_jawaban(request, id):
    print("hai km lg di add jawaban")
    # form_jawaban = JawabanForm(request.POST)
    jawaban = request.POST.get('jawaban')
    print(jawaban)
    pertanyaan = Pertanyaan.objects.get(id=id)
    pertanyaan.is_answered = True
    pertanyaan.save()
    
    new_faq = FAQ(pertanyaan=pertanyaan, jawaban=jawaban)
    new_faq.save()
    print(new_faq.pertanyaan.teks_pertanyaan)

    res = { "model": "customer_service.faq", 
            "pk": new_faq.pk, 
            "fields": { "pertanyaan": { "model": "customer_service.pertanyaan", 
                                        "pk": new_faq.pertanyaan.pk, 
                                        "fields": { "kategori": new_faq.pertanyaan.kategori, 
                                                    "teks_pertanyaan": new_faq.pertanyaan.teks_pertanyaan, 
                                                    "is_answered": new_faq.pertanyaan.is_answered } }, 
                        "jawaban": new_faq.jawaban } }
    # res = serializers.serialize('json', [new_faq])
    print(res)
    return JsonResponse(res)

    # return HttpResponseRedirect(reverse('customer_service:show_faq'))

def jsonFAQ(request):
    print("jsonfaq")
    # faqs = json.loads(serializers.serialize('json', FAQ.objects.all()))
    # print(faqs)
    # # for faq in faqs:
    # #     for x in faq:
    # #         id = faq["fields"]["pertanyaan"]
    # #         qs = Pertanyaan.objects.get(pk=id)
    # #         dictQS = { "model": "customer_service.pertanyaan", 
    # #                     "pk": qs.pk, 
    # #                     "fields": { "kategori": qs.kategori, 
    # #                                 "teks_pertanyaan": qs.teks_pertanyaan, 
    # #                                 "is_answered": qs.is_answered } }
    # #         faq["fields"]["pertanyaan"] = dictQS

    # return JsonResponse(faqs, safe=False)
    # print(serializers.serialize('json', FAQ.objects.all()))
    return HttpResponse(serializers.serialize('json', FAQ.objects.all(), use_natural_foreign_keys=True), content_type='application/json')

def jsonPertanyaan(request):
    print("jsonpertanyaan")
    questions = Pertanyaan.objects.filter(is_answered=False)
    print(questions)
    return HttpResponse(serializers.serialize('json', questions), content_type='application/json')

@login_required(login_url='/general_user/login/')
def add_pertanyaan(request):
    print("hai km lg di add pert")
    kategori = request.POST.get('kategori')
    teks_pertanyaan = request.POST.get('teks_pertanyaan')
    new_pertanyaan = Pertanyaan(kategori=kategori, teks_pertanyaan=teks_pertanyaan)
    new_pertanyaan.save()

    res = { "model": "customer_service.pertanyaan", 
            "pk": new_pertanyaan.pk, 
            "fields": { "kategori": new_pertanyaan.kategori, 
                        "teks_pertanyaan": new_pertanyaan.teks_pertanyaan, 
                        "is_answered": new_pertanyaan.is_answered } }
   
    return JsonResponse(res)

#     return HttpResponse()

    # return redirect('customer_service:show_faq')
    # HttpResponseRedirect(reverse('customer_service:show_faq'))

# @login_required(login_url='/general_user/login/')
# def add_pertanyaan(request):
#     if request.method == "POST":
#         new_pertanyaan = PertanyaanForm(request.POST)
#         if new_pertanyaan.is_valid():
#             new_pertanyaan.save(commit=False)
#             new_pertanyaan.save()

#             res = { "model": "customer_service.pertanyaan", 
#                     "pk": new_pertanyaan.pk, 
#                     "fields": { "kategori": new_pertanyaan.kategori, 
#                                 "teks_pertanyaan": new_pertanyaan.teks_pertanyaan, 
#                                 "is_answered": new_pertanyaan.is_answered } }

#             return JsonResponse(res)


# @login_required(login_url='/general_user/login/')
# def add_jawaban(request, id):
#     if request.method == "POST":
#         form_jawaban = JawabanForm(request.POST)
#         if form_jawaban.is_valid():
#             new_faq = form_jawaban.save(commit=False)
#             pertanyaan = Pertanyaan.objects.get(id=id)
#             pertanyaan.is_answered = True
#             pertanyaan.save()
#             new_faq.pertanyaan = pertanyaan
#             new_faq.save()

#             res = { "model": "customer_service.faq", 
#                 "pk": new_faq.pk, 
#                 "fields": { "pertanyaan": { "model": "customer_service.pertanyaan", 
#                                             "pk": new_faq.pertanyaan.pk, 
#                                             "fields": { "kategori": new_faq.pertanyaan.kategori, 
#                                                         "teks_pertanyaan": new_faq.pertanyaan.teks_pertanyaan, 
#                                                         "is_answered": new_faq.pertanyaan.is_answered } }, 
#                             "jawaban": new_faq.jawaban } }

#             return JsonResponse(res)
