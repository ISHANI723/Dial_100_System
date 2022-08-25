from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import form1Detail, Operations, History, FRV, FRV_Assigned ,Frv_Draw
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
try:
    MAPS_API_KEY = os.environ['MAPS_API_KEY']
except KeyError:
    print("MAPS_API_KEY is not set")
    exit()

FRV_suggestion = {
    'accident': 'Ambulance, Police',
    'fire': 'Fire Bridage, Ambulance, Police',
    'robbery': 'Police',
    'kidnapping': 'Police',
    'health': 'Amblance',
    'others': '',
}

#following are predefind user login  each have password test@123
user='none'
form1array=['prajwal','hritvik1','bang1','bhate1','ishani1','ritik1']
form2array=['hritvik','bang2','bhate2','ishani2','ritik2','prajwal2']

Elat_list=[]
Elng_list=[]
E_dict={}
def index(request):
    if request.method == 'POST':
        post = form1Detail()
        post.Dialer_Name = request.POST.get('Dialer_Name')
        post.Dialer_Address = request.POST.get('Dialer_Address')
        post.Describe_call = request.POST.get('Describe_call')
        post.Incident_Type = request.POST.get('Incident_Type')
        post.Phone_Number = request.POST.get('Phone_Number')
        post.Division = request.POST.get('Division')
        post.District = request.POST.get('District')
        post.Incident_Address = request.POST.get('Incident_Address')
        post.date = datetime.today()
        post.frv_req = FRV_suggestion[request.POST.get('Incident_Type')]

        post.save()
        messages.success(request, "Details Saved Successfully.",
                         extra_tags='alert alert-success alert-dismissible fade show')

    return render(request, 'form1.html', {'user': user})


def form2(request):
    datas = form1Detail.objects.all()
    operations = Operations.objects.all()
    history = History.objects.all()

    return render(request, 'supervisor.html', {'datas': datas[::-1], 'operations': operations[::-1], 'history': history[::-1], 'user': user, 'MAPS_API_KEY':MAPS_API_KEY })


def move_to_history(request, case_id):
    try:
        case = form1Detail.objects.get(id=case_id)
    except:
        case = get_object_or_404(Operations, id=case_id)
    history = History()
    history.id = case.id
    history.Dialer_Name = case.Dialer_Name
    history.Dialer_Address = case.Dialer_Address
    history.Describe_call = case.Describe_call
    history.Incident_Type = case.Incident_Type
    history.Phone_Number = case.Phone_Number
    history.Division = case.Division
    history.District = case.District
    history.Incident_Address = case.Incident_Address
    history.date = case.date

    history.save()

    try:
        history.frvs = case.frvs
    except:
        pass

    history.save()
    case.delete()

    messages.success(request, "Task Completed.",
                     extra_tags='alert alert-success alert-dismissible fade show')

    return redirect('/form2')


def create_frv(request):
    if request.method == 'POST':
        frv = FRV()
        frv.FRV_Type = request.POST.get("frv_type")
        frv.Driver_Name = request.POST.get("name")
        frv.lat = request.POST.get("lat")
        frv.lng = request.POST.get("lng")
        frv.save()

        messages.success(request, "FRV Details Saved Successfully.",
                         extra_tags='alert alert-success alert-dismissible fade show')

    return render(request, 'add_frv.html')


def get_case_location(request):
    if request.method == 'GET':
        case_id = request.GET.get('case_id')
        try:
            case = form1Detail.objects.get(id=case_id)
        except:
            case = Operations(id=case_id)

        if case.lat and case.lng:
            return JsonResponse({'status': 'OK', 'case_id':case_id, 'location': {'lat': case.lat, 'lng': case.lng}})
        else:
            return JsonResponse({'status': 'LOCATION_NOT_SET', 'case_id':case_id})


def set_case_location(request):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        try:
            case = form1Detail.objects.get(id=case_id)
        except:
            case = Operations(id=case_id)

        case.lat = lat
        case.lng = lng
        case.save()

        return JsonResponse({'status': 'OK'})

def assign_frv(request):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        frv_name=request.POST.get('frv_name')
        frv = FRV.objects.filter(Driver_Name=frv_name.replace(" ", "_"))[0]
        frv_assign=FRV_Assigned()
        frv_assign.FRV_Type = frv.FRV_Type
        frv_assign.Driver_Name = frv.Driver_Name
        frv_assign.lat=frv.lat
        frv_assign.lng=frv.lng
        frv_assign.case_id=case_id
        frv_assign.end_lat=lat
        frv_assign.end_lng=lng
        frv_assign.save()
        try:
            try:
                case = form1Detail.objects.get(id=case_id)
                operations = Operations()
                operations.id = case.id
                operations.Dialer_Name = case.Dialer_Name
                operations.Dialer_Address = case.Dialer_Address
                operations.Describe_call = case.Describe_call
                operations.Incident_Type = case.Incident_Type
                operations.Phone_Number = case.Phone_Number
                operations.Division = case.Division
                operations.District = case.District
                operations.Incident_Address = case.Incident_Address
                operations.date = case.date
                operations.lat=case.lat
                operations.lng=case.lng

                operations.save()
                operations.frvs.add(frv)
                case.delete()
            except:
                operations = Operations.objects.get(id=case_id)
                operations.frvs.add(frv)
            finally:
                return JsonResponse({'status': 'OK'})
        except Exception as e:
            return JsonResponse({'status': e})



def driver(request):
    # to find starting and ending location from database

    global user
    user=str(user)

    if not user:
        return redirect('/login')

    driver_ll=FRV_Assigned.objects.filter(Driver_Name=user)
    global Slat
    global Slng
    global type
    global Elat
    global Elng
    global Elat_list
    global Elng_list
    global E_dict
    global  status
    status='not started'
    user = user.replace("_", " ")

    for s in driver_ll:
        Slat=s.lat
        Slng=s.lng
        type =s.FRV_Type
        E_dict[s.case_id]=[s.end_lat,s.end_lng]
        Elat_list.append(s.end_lat)
        Elng_list.append(s.end_lng)

    if request.method=="POST":
        status=request.POST.get('status')
        lat=request.POST.get('lat')
        lng=request.POST.get('lng')
        if lat and lng:
            user = user.replace(" ", "_")
            frvl=FRV.objects.filter(Driver_Name=user)
            frvl.update(lat=lat)
            frvl.update(lng=lng)
        if status:
            print(status)
            user = user.replace(" ", "_")
            x = FRV_Assigned.objects.filter(Driver_Name=user)
            x.filter(end_lat=Elat).update(status=status)
            if status=='end':
                return render(request, 'driverRecord.html', {'user': user, 'driver_ll': driver_ll})

            else:
                return JsonResponse({'status': 'OK'})
        ite=request.POST.get("i")
        Elat = E_dict[ite][0]
        Elng = E_dict[ite][1]

        user = user.replace(" ", "_")
        x=FRV_Assigned.objects.filter(Driver_Name=user)
        x.filter(end_lat=Elat).update(status='assigned')
        return render(request,'driver.html', {'user': user,'ite':ite, 'Slat':Slat,"Slng":Slng, 'Elat':Elat,"Elng":Elng,'type':type, 'MAPS_API_KEY':MAPS_API_KEY})
    else:
        return render(request,'driverRecord.html',{'user':user,'driver_ll':driver_ll})

def home(request):
    return render(request, 'home.html')


def signup_view(request):
    global user
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log user in
            login(request, user)
            return render(request, 'menu.html', {"user": user})
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})


def login_view(request):
    global user
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in
            user=form.get_user()
            login(request,user)
            user=str(user)
            if user in form1array:
                return  redirect(index)
            elif 'form1' in user or 'operator' in user:
                return redirect(index)
            elif user in form2array:
                return  redirect(form2)
            elif 'form2' in user or 'supervisor' in user:
                return redirect(form2)
            else:
                return redirect(driver)
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})


def logout_view(request):
        logout(request)
        return redirect('login')


def menu_view(request):
    return render(request,'menu.html')


#[[{lst,},true1|false], +]

def newroad(request):
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        online=request.POST.get('online')
        x = Frv_Draw.objects.filter(Name='user')
        if lat and lng:
            location={'lat':lat,'lng':lng}
            result=[location,online]
            print(location)
            for x1 in x:
                a=eval(x1.Cord)
                if len(a)==0:
                    x1.Cord = str(a)
                    x1.save()
                print(lat)
                print(lng)
                if (lat!=a[-1][0]['lat'] and lng!=a[-1][0]['lng'] ):
                 a.append(result)
                 x1.Cord=str(a)
                 x1.save()
    return render(request,'newroot.html')