from django.contrib import admin
from .models import form1Detail, Operations, History, FRV,FRV_Assigned ,Frv_Draw
# Register your models here.

admin.site.register(form1Detail)
admin.site.register(Operations)
admin.site.register(History)
admin.site.register(FRV)
admin.site.register(FRV_Assigned)
admin.site.register(Frv_Draw)
