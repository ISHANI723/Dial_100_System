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

global form1array
form1array=['prajwal','hritvik1','bang1','bhate1','ishani1','ritik1']
global form2array
form2array=['hritvik','bang2','bhate2','ishani2','ritik2','prajwal2']
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

    coordinates = {

        'Ohio Hospital':
            {
                'lat': 22.578305383029246, 'lng': 88.47703737631674}

        ,
        'Bhagirathi Neotia Woman and Child Care Centre':
            {
                'lat': 22.58007151014703, 'lng': 88.47554810340063}
        ,
        'New Town Police Station':
            {
                'lat': 22.579454581993136, 'lng': 88.4789031781252}

        ,
        'Technocity Police Station':
            {
                'lat': 22.564871517979633, 'lng': 88.51563870949663}

        ,
        'Newtown - Rajarhat Fire Station':
            {
                'lat': 22.579783567356824, 'lng': 88.45847724147374}

        ,
        'Fire Brigade Sector 5':
            {
                'lat': 22.56926551832623, 'lng': 88.43222217838807}

          }
    global user
    user=str(user)
    user = user.replace("_", " ")
    lat=coordinates[user]['lat']
    lng=coordinates[user]['lng']

    return render(request,'driver.html',{'user':user,'lat':lat,'lng':lng})



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