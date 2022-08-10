from django.shortcuts import render
from datetime import datetime
from .models import form1Detail


# Create your views here.

def index(request):
        if request.method == 'POST':
            post=form1Detail()
            post.Dialer_Name = request.POST.get('Dialer_Name')
            post.Dialer_Address = request.POST.get('Dialer_Address')
            post.Describe_call = request.POST.get('Describe_call')
            post.Incident_Type = request.POST.get('Incident_Type')
            post.Phone_Number = request.POST.get('Phone_Number')
            post.Division = request.POST.get('Division')
            post.District = request.POST.get('District')
            post.Incident_Address = request.POST.get('Incident_Address')
            post.date = datetime.today()
            #newEntruy = form1Detail(Dialer_Name=Dialer_Name, Dialer_Address=Dialer_Address,
            #  #                       Describe_call=Describe_call,Incident_Type=Incident_Type,
            #                         Phone_Number=Phone_Number, Division=Division,
            #                           District=District,Incident_Address=Incident_Address,
            #                         date = datetime.today())
            post.save()
        return render(request,'form1.html')

def form2(request):
    datas=form1Detail.objects.all()
    return render(request,'form2.html',{'datas':datas})