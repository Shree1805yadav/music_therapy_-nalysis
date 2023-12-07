from django.contrib import admin
from .models import FormData, Recommendation

# Register your models here.

class FormDataModel(admin.ModelAdmin):
    list_display = ('user','Age','Gender','MobileNo','MailId','Problems','Symptoms')

admin.site.register(FormData,FormDataModel)
admin.site.register(Recommendation)