from django.db import models

# Create your models here.
class form1Detail(models.Model):
    Dialer_Name=models.CharField(max_length=300)
    Dialer_Address=models.TextField(max_length=500)
    Describe_call=models.TextField(max_length=500)
    Incident_Type=models.CharField(max_length=500)
    Phone_Number=models.CharField(max_length=10)
    Division=models.CharField(max_length=500)
    District=models.CharField(max_length=500)
    Incident_Address=models.TextField(max_length=500)
    date = models.DateField()
