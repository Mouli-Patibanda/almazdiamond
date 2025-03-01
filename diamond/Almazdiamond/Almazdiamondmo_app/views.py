from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
#Create your views here.
def test_view(request):
    return render(request,'Homemain.html')

def test_2(request):
    return HttpResponse('working ')
def login(request):

    return render(request,'login.html')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def ring_settings_admin(request):
    ring_settings=RingSettings.objects.all()
    context={'ring_settings':ring_settings}
    return render(request,'ring_settings_admin.html',context)

def add_edit_ring_settings(request,id=None):
    ring_settings=ring_details=None
    if request.method=='POST':
        defaults={
            "ring_settings":request.POST.get('ring_settings',''),
            "metal_type":request.POST.get('metal_type',''),
            "shapes":request.POST.get('shapes',''),
            "name":request.POST.get('name',''),
            "description":request.POST.get('description',''),
            "price":request.POST.get('price',0),
            'currency':request.POST.get('currency','USD'),
           
        }
        if request.FILES.get('image'):
            defaults["image"]=request.FILES.get('image')
        ring,created=RingSettings.objects.update_or_create(
            id=id,
            defaults=defaults
        )
        if ring:
            files=request.FILES.getlist('files',[])
            for i in files:
                RingDetails.objects.create(
                    ring=ring,
                    file=i
                )

        return redirect('ring_settings_admin')
    if id:
        ring_settings=RingSettings.objects.filter(id=id).first()
        if ring_settings:
            ring_details=RingDetails.objects.filter(ring=ring_settings)
    return render(request,'add_edit_ring_setting.html',{"ring_settings":ring_settings,"setting_types":SETTING_TYPES,"metal_types":METAL_TYPES,"ring_shapes":RING_SHAPES,"currency":CURRENCY_CHOICES,"ring_details":ring_details,"id":id})

def delete_ring_setting(request,id):
    RingSettings.objects.filter(id=id).delete()
    return redirect('ring_settings_admin')

def delete_ring_files(reques,rs_id,id=None):
    if rs_id and id:
        ringdetails=RingDetails.objects.filter(ring_id=rs_id,id=id).first()
        if ringdetails:
           ringdetails.delete()
    elif rs_id:
        ring_settings=RingSettings.objects.filter(id=rs_id).first()
        if ring_settings:
            ring_settings.image=None
            ring_settings.save()
    return redirect(reverse('edit_ring',kwargs={"id":rs_id}))

def stone_admin(request):
    stones=Stone.objects.all()
    context={'stones':stones}
    return render(request,'stone_admin.html',context)

def add_edit_stone(request,id=None):
    stone=stone_details=None
    if request.method=='POST':
        defaults={
            "stone_name":request.POST.get('stone_name',''),
            "description":request.POST.get('description',''),
            "stone_type":request.POST.get('stone_type',''),
            "stone_shape":request.POST.get('stone_shape',''),
            "stone_carat":14,
            "stone_price":request.POST.get('stone_price',0),
            "stone_cut":request.POST.get('stone_cut',''),
            "stone_clarity":request.POST.get('stone_clarity',""),
            'currency':request.POST.get('currency','USD')
           
        }
        if request.FILES.get('image'):
            defaults["image"]=request.FILES.get('image')
        stone,created=Stone.objects.update_or_create(
            id=id,
            defaults=defaults
        )
        if stone:
            files=request.FILES.getlist('files',[])
            for i in files:
                StoneDetails.objects.create(
                    stone=stone,
                    file=i
                )

        return redirect('stone_admin')
    if id:
        stone=Stone.objects.filter(id=id).first()
        if stone:
            stone_details=StoneDetails.objects.filter(stone=stone)
    return render(request,'add_edit_stone.html',{"stone":stone,"stone_cuts":STONE_CUT_CHOICES,"stone_clarities":STONE_CLARITY,"stone_shapes":STONE_SHAPES,"currency":CURRENCY_CHOICES,"stone_details":stone_details,"id":id})

def delete_stone(request,id):
    Stone.objects.filter(id=id).delete()
    return redirect('stone_admin')

def delete_stone_files(request,s_id,id=None):
    if s_id and id:
        stonedetails=StoneDetails.objects.filter(stone_id=s_id,id=id).first()
        if stonedetails:
           stonedetails.delete()
    elif s_id:
        stone=Stone.objects.filter(id=s_id).first()
        if stone:
            stone.image=None
            stone.save()
    return redirect(reverse('edit_stone',kwargs={"id":s_id}))

def ring_stone_combination_admin(request):
    combinations=Combination.objects.all()
    print(combinations,"lll")
    context={"combinations":combinations}
    return render(request,'combination_admin.html',context)
def add_edit_combination(request,id=None):
    combination=combination_files=None
    if request.method=='POST':
        defaults={
            "ring_id":request.POST.get('ring_id'),
            "stone_id":request.POST.get('stone_id'),
            "price":request.POST.get('price',0.0),
            "currency":request.POST.get('currency','USD')
        }
        combination,created=Combination.objects.update_or_create(
            id=id,
            defaults=defaults

        )
        if combination:
            files=request.FILES.getlist('files',[])
            for i in files:
                CombinationFiles.objects.create(
                    combination_id=combination.id,
                    files=i
                )
        return redirect('ring_stone_combination_admin')
    if id:
        combination=Combination.objects.filter(id=id).first()
        if combination:
            combination_files=CombinationFiles.objects.filter(combination_id=combination.id)
    stones=Stone.objects.all().only('id','stone_name')
    ring_settings=RingSettings.objects.all().only('id','name')
    print(ring_settings,stones,"lll")
    context={
        "combination_files":combination_files,
        "combination":combination,
        "id":id,
        "stones":stones,
        "ring_settings":ring_settings,
        "currency":CURRENCY_CHOICES
    }
    return render(request,'add_edit_combination.html',context) 

def delete_combination(request,id):
    combination=Combination.objects.filter(id=id).first()
    if combination:
        combination.delete()
    return redirect('ring_stone_combination_admin')

def delete_combination_files(request,c_id,id):
    if c_id and id:
        combinationfile=CombinationFiles.objects.filter(combination_id=c_id,id=id).first()
        if combinationfile:
            combinationfile.delete()
    return redirect(reverse('edit_combination',kwargs={"id":c_id}))

def ring_settings(request,stone_id=None):
    ring_settings=RingSettings.objects.all()
    return render(request,'setting.html',{"ring_settings":ring_settings,"settings":SETTING_TYPES,"stone_id":stone_id})

def get_more_ring_details(request,id,stone_id=None):
    ring_details=RingDetails.objects.filter(ring_id=id)
    ring=RingSettings.objects.filter(id=id).first()
    return render(request,'ring_details.html',{"ring_details":ring_details,"ring":ring,"ring_shapes":RING_SHAPES,"stone_id":stone_id})

def combination_stone_ring(request,stone_id,ring_id):
    combination=Combination.objects.filter(stone_id=stone_id,ring_id=ring_id).first()
    combination_details=CombinationFiles.objects.filter(combination_id=combination)
    print(combination_details,"lll")
    return render(request,'combination_stone_ring.html',{"combination":combination,"combination_details":combination_details,"stone_id":stone_id,"ring_id":ring_id})

def stones(request,ring_id=None):
    stones=Stone.objects.all()
    return render(request,'stone.html',{"stones":stones,"ring_id":ring_id,"stone_shapes":STONE_SHAPES,"stone_cuts":STONE_CUT_CHOICES,"stone_clarity":STONE_CLARITY})

def get_more_stone_details(request,id,ring_id=None):
    stone_details=StoneDetails.objects.filter(stone_id=id)
    print(stone_details,"mmm")
    stone=Stone.objects.filter(id=id).first()
    return render(request,'stone_details.html',{"stone_details":stone_details,"stone":stone,"stone_shapes":STONE_SHAPES,"ring_id":ring_id})