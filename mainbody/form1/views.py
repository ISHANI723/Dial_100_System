from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import form1Detail, Operations, History, FRV, FRV_Assigned
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

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

    return render(request, 'supervisor.html', {'datas': datas[::-1], 'operations': operations[::-1], 'history': history[::-1], 'user': user})


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
        frv = FRV.objects.get(Driver_Name=frv_name.replace(" ", "_"))            
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
    driver_ll=FRV_Assigned.objects.filter(Driver_Name=user)
    global Slat
    global Slng
    global type
    global Elat
    global Elng
    global Elat_list
    global Elng_list
    user = user.replace("_", " ")

    for s in driver_ll:
        Slat=s.lat
        Slng=s.lng
        type =s.FRV_Type
        Elat_list.append(s.end_lat)
        Elng_list.append(s.end_lng)

    if request.method=="POST":
        ite=request.POST.get("i")
        ite=int(ite)-1
        print(ite)
        Elat = Elat_list[ite]
        Elng = Elng_list[ite]

        return render(request, 'driver.html', {'user': user, 'Slat':Slat,"Slng":Slng, 'Elat':Elat,"Elng":Elng,'type':type})
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
    if request.method == 'POST':
        logout(request)
        return render(request,"login.html")


def menu_view(request):
    return render(request,'menu.html')
