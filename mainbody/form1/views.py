from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from .models import form1Detail, Operations, History, FRV
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login ,logout
FRV_suggestion = {
    'accident': 'Ambulance, Police',
    'fire': 'Fire Bridage, Ambulance, Police',
    'robbery': 'Police',
    'kidnapping': 'Police',
    'health': 'Amblance',
    'others': '',
}
# Create your views here.
#following are predefind user login  each have password test@123
global user
user='none'
global Elat
global Elng
global form1array
form1array=['prajwal','hritvik1','bang1','bhate1','ishani1','ritik1']
global form2array
form2array=['hritvik','bang2','bhate2','ishani2','ritik2','prajwal2']

global Elat_list
Elat_list=[]
global Elng_list
Elng_list=[]
#following are predefind user login
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
    
    return render(request, 'form1.html',{'user':user})


def form2(request):
    datas = form1Detail.objects.all()
    operations = Operations.objects.all()
    history = History.objects.all()

    return render(request, 'supervisor.html', {'datas': datas[::-1], 'operations': operations[::-1], 'history': history[::-1],'user':user})


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
        frv=FRV()
        frv.FRV_Type = request.POST.get("frv_type")
        frv.FRV_Plate_No = request.POST.get("plate_no")
        frv.Driver_Name = request.POST.get("name")
        frv.Driver_Number = request.POST.get("phone_no")
        frv.lat = request.POST.get("lat")
        frv.lng = request.POST.get("lng")
        frv.save()

        messages.success(request, "FRV Details Saved Successfully.",
                         extra_tags='alert alert-success alert-dismissible fade show')
    
    return render(request, 'add_frv.html')


FRV_TYPES = ['ambulance', 'police_car', 'fire_brigade' ]
def list_frvs(request, frv_type, case_id):
    case= get_object_or_404(form1Detail, id=case_id)
    frvs= FRV.objects.filter(FRV_Type=frv_type).values()



def driver(request):
    # to find startind and endig locarion from database

    global user
    user=str(user)
    driver_ll=FRV.objects.filter(Driver_Name=user)
    global Slat
    global Slng
    global type
    global Elat
    global Elng
    global Elat_list
    global Elng_list
    user = user.replace("_", " ")
    # following 2 line may not work as we may may have many cases assign to single frv
    for s in driver_ll:
        Slat=s.lat
        Slng=s.lng
        type =s.FRV_Type
    for x in driver_ll:
        Elat_list.append(x.end_lat)
        Elng_list.append(x.end_lng)
        # Elat = x.end_lat
        # Elng = x.end_lng
        # print(Elat_list)
        # print(Elng_list)
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
    return render(request,'home.html')




def signup_view(request):
    global user
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            #log user in
            login(request, user)
            return render(request,'menu.html',{"user":user})
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{"form":form})


def login_view(request):
    global user
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
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
    if request.method=='POST':
        logout(request)
        return render(request,"login.html")


def menu_view(request):
    return render(request,'menu.html')

