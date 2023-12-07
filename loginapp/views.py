from xmlrpc.client import boolean
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.api import error
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView

from loginapp.models import FormData
from .form import SignupForm
from django.utils.encoding import force_bytes
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import FormData, Recommendation
from django.core.paginator import Paginator
import pandas as pd
import datetime
# Ml function


def time_in_range(start, end, current):
    if start <= end:
        return start <= current <= end
    else:
        return start <= current or current <= end


# django functions
def index(request):
    currentuser = request.user
    userdata = FormData.objects.filter(user=currentuser)
    length = len(userdata)
    print("length",length)
    boolean_value=length>0
   
    content={

       "con": boolean_value
        
    }
    print(content)
    return render(request, 'index.html',content)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email = form.cleaned_data.get('email')
            user.save()
            # '127.0.0.1:8000'                                           #get_current_site(request)
            current_site = get_current_site(request)
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,  # '127.0.0.1:8000' , current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),


                'token': account_activation_token.make_token(user),
            })
            subject = 'Activate Your  Account'
            user.email_user(subject, message)

            emailsend = EmailMessage(
                subject, message, from_email=settings.EMAIL_HOST_USER, to=[email])
            emailsend.send()
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('account_activation_sent')

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def LoginUser(request):
    if request.user.is_anonymous == False:
        return redirect('/form')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            messages.add_message(request, messages.SUCCESS,
                                 "Logged in successfull ")
            return redirect('/')
        else:
            # No backend authenticated the credentials
            messages.add_message(request, messages.ERROR,
                                 "You don't have an account.")

    return render(request, 'login.html')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        # login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def Logout(request):
    logout(request)
    return redirect("/")


def Form(request):
    
    
    if request.user.is_anonymous:
        return redirect("/login")
    currentuser = request.user
    # data=Recommendation.objects.filter(user=currentuser)
    # data.delete()
    userdata = FormData.objects.filter(user=currentuser)
    length = len(userdata)
    if length > 0:
        result = userdata[length-1]
        context = {
            "age": result.Age,
            "gender": result.Gender,
            "mobileno": result.MobileNo,
            "mailid": result.MailId
        }
    else:
        result = ""
        context = {
            "age": result,
            "gender": result,
            "mobileno": result,
            "mailid": result
        }
    return render(request, 'form.html', context)


def recom(request):
    user=request.user
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        
        
       
        user = request.user.username
        Age = request.POST.get('age')
        Gender = request.POST.get('gender')
        MobileNo = request.POST.get('mobileno')
        MailId = request.POST.get('mailid')
        Problems = request.POST.getlist('problems')
       

        Symptoms = request.POST.getlist('symptoms')
       

        # ML code
        EXCEL_FILE = 'D:\\Music project new\\doctor\\database music.xlsx'
        df = pd.read_excel(EXCEL_FILE)
        df.sort_values("Average", axis = 0, ascending = False,inplace = True, na_position ='first')
        df.to_excel("D:\\Music project new\\doctor\\database mu.xlsx", index=False)
        a = len(df.index)
      

        for i in range(0, a):
           
            for j in range(0, len(Problems)):

                if Problems[j] == (df.iat[i, 8]):
                    start = datetime.time(df.iat[i, 6], 0, 0)
                    end = datetime.time(df.iat[i, 7], 0, 0)
                    current = datetime.datetime.now().time()
                    result = time_in_range(start, end, current)
                    if result == True: 
                        
                        recom=Recommendation(user=user,music_id=df.iat[i,0], raag=df.iat[i, 1], type=df.iat[i,5],music=df.iat[i, 10],music_path=df.iat[i,4])
                        recom.save()
                                
                        print("Recommended Raag & Audio : " +
                              df.iat[i, 9]+"\\"+df.iat[i, 5]+"\\"+df.iat[i, 4]+"\\"+str(df.iat[i,13]) +"\n")

        data = FormData(user=user, Age=Age, Gender=Gender, MobileNo=MobileNo,
                        MailId=MailId, Problems=Problems, Symptoms=Symptoms, Recommendation="")
        data.save()
       
     
   
      

        # return redirect('/casepaper')
    content=Recommendation.objects.filter(user=user)
    p=Paginator(Recommendation.objects.filter(user=user).order_by('-createdAt'),10)
    page_num=request.GET.get('page')
    print("page",page_num)
    page=p.get_page(page_num)
    print(page)
    return render(request, 'recom.html',{"content":page})


def Convert(string):
    string.replace('[','')
    string.replace(']','')
    string.replace('\'','')
    string.replace('{','')
    string.replace('}','')
    li = list(string.split(","))
    return li

def casePaper(request):
    if request.user.is_anonymous:
        return redirect("/")
    currentuser = request.user
    userdata = FormData.objects.filter(user=currentuser)
    l = len(userdata)
    userresult = userdata[l-1]
    recomdata = Recommendation.objects.filter(user=currentuser)

    lista = []

    


    length = len(userdata)
    if length > 0:
        result = userdata[length-1]
        data = result.Problems
        data = data.replace('[','')
        data = data.replace(']','')
        data = data.replace('\'','')
        data = data.replace(' ','')
        datab = data.split(',')
        print(type(datab))
        data1 = result.Symptoms
        data1 = data1.replace('[','')
        data1 = data1.replace(']','')
        data1 = data1.replace('\'',' ')
        data1 = data1.replace('?','')
        # data1 = data1.replace(' ','')
        datab1 = data1.split(',')
        print(type(datab1))
        for i in range(len(datab)):
            print(datab[i])
        
        EXCEL_FILE = 'D:\\Music project new\\doctor\\database music.xlsx'
        df = pd.read_excel(EXCEL_FILE)
        a=len(df.index)
        print(a)
        count=0
        for i in range(0,a):
            for j in range(0,len(datab)):
                if datab[j] == (df.iat[i,9]):
                
                   
                    b = "Raag:"+df.iat[i,2]+  "\n        \ Vadi/Sanwadi:"+df.iat[i,3]+"           Thaat:"+df.iat[i,4]
                    # b= ("{:<50} {:<50} {:<50}".format( "Raag:" +df.iat[i,2], "    Vadi/Sanwadi:"+df.iat[i,3],"   Thaat:"+df.iat[i,4]))
                   
                       
                    lista.append(b)
                    print(lista)
                  
        # c =   list(set(lista))
        c=set(list(lista))
        c=set(list(c)[:5])
    
          
       

        context = {
            "age": result.Age,
            "gender": result.Gender,
            "mobileno": result.MobileNo,
            "mailid": result.MailId,
            "caseno": length,
            "problems": datab,
            "symptoms": datab1,
            "length": length,
            "solution": c
        }
    else:
        result = ""
        context = {
            "age": result,
            "gender": result,
            "mobileno": result,
            "mailid": result,
            "caseno": result,
            "problems": result,
            "symptoms": result,
            "length": length,
            "solution": result
        }
    return render(request, 'casepaper.html', context)


def review(request,pk):
    print(pk)
    beforeheartrate=0
    beforeoxygenlevel=0
    afterheartrate=0 
    afteroxygenlevel=0 
    beforesystoliclevel=0 
    beforediastoliclevel=0 
    beforeglucoselevel=0 
    afterdiastoliclevel=0
    afterglucoselevel=0 
    aftersystoliclevel=0
    if request.method == 'POST':
        rating = request.POST.get('rating')
        beforeheartrate = int(request.POST.get('beforeheartrate'))
        beforeoxygenlevel =int( request.POST.get('beforeoxygenlevel'))
        beforediastoliclevel=int(request.POST.get('bdia'))
      
        
        beforeglucoselevel= int(request.POST.get('beforeglucoselevel'))
        beforesystoliclevel  = int(request.POST.get('beforesstoliclevel'))
        afterheartrate = int(request.POST.get('afterheartrate'))
        afteroxygenlevel =int (request.POST.get('afteroxygenlevel'))
        aftersystoliclevel =int (request.POST.get('aftersstoliclevel'))
        afterdiastoliclevel=int(request.POST.get('adia'))
        afterglucoselevel=int(request.POST.get('aglu'))

        EXCEL_FILE = 'D:\\Music project new\\doctor\\database music.xlsx'
        df = pd.read_excel(EXCEL_FILE,index_col = False)
        pk -=1
        print(type(df.iat[pk,11]))
        print(type(rating))
        print(df.iat[pk,11])
        print(rating)
        print(float(rating))
        print(type(float(rating)))
        df.iat[pk,11] = float(df.iat[pk,11]) + float(rating)
        print(df.iat[pk,11])
        df.iat[pk,12] = int(df.iat[pk,12]) + 1
        df.iat[pk,13] = int(df.iat[pk,11])/int(df.iat[pk,12])
        df.to_excel("D:\\Music project new\\doctor\\database music.xlsx", index=False)

        print(rating, beforeheartrate, beforeoxygenlevel,
              afterheartrate, afteroxygenlevel,beforesystoliclevel,beforediastoliclevel,beforeglucoselevel,afterdiastoliclevel,afterglucoselevel,aftersystoliclevel)

        heartratestatus = ""
        oxygenstatus = ""

    if beforeheartrate>=60 and beforeheartrate<=100:
        heartratebefore=1
    else:
        heartratebefore=0
    
    if afterheartrate>=60 and afterheartrate<=100:
        heartrateafter=1
    else:
        heartrateafter=0
    
    if heartratebefore==heartrateafter:
        heartratestatus = 'No change'
    elif heartratebefore==0 and heartrateafter==1:
        heartratestatus = 'Improved'
    elif heartratebefore==1 and heartrateafter==0:
        heartratestatus = 'Worsened'

    
    if beforeoxygenlevel>=95 and beforeoxygenlevel<=100:
        oxygenbefore=1
    else:
        oxygenbefore=0
    
    if afteroxygenlevel>=95 and afteroxygenlevel<=100:
        oxygenafter=1
    else:
        oxygenafter=0
    
    if oxygenbefore==oxygenafter:
        oxygenstatus = 'No change'
    elif oxygenbefore==0 and oxygenafter==1:
        oxygenstatus = 'Improved'
    elif oxygenbefore==1 and oxygenafter==0:
        oxygenstatus = 'Worsened'
    
    if beforesystoliclevel<=120:
        systolicbefore=1
    else:
        systolicbefore=0
    
    if aftersystoliclevel<=120:
        systolicafter=1
    else:
        systolicafter=0
    
    if systolicbefore==systolicafter:
        systolicstatus = 'No change'
    elif systolicbefore==0 and systolicafter==1:
        systolicstatus = 'Improved'
    elif systolicbefore==1 and systolicafter==0:
        systolicstatus = 'Worsened'
    
    if beforediastoliclevel<=80:
        diastolicbefore=1
    else:
        diastolicbefore=0
    
    if afterdiastoliclevel<=80:
        diastolicafter=1
    else:
        diastolicafter=0
    
    if diastolicbefore==diastolicafter:
         diastolicstatus = 'No change'
    elif diastolicbefore==0 and diastolicafter==1:
        diastolicstatus = 'Improved'
    elif diastolicbefore==1 and diastolicafter==0:
         diastolicstatus = 'Worsened'
    
    if beforeglucoselevel<=140:
         glucosebefore=1
    else:
         glucosebefore=0
    
    if afterglucoselevel<=140:
         glucoseafter=1
    else:
         glucoseafter=0
    
    if glucosebefore==glucoseafter:
        glucosestatus = 'No change'
    elif glucosebefore==0 and glucoseafter==1:
        glucosestatus = 'Improved'
    elif glucosebefore==1 and glucoseafter==0:
        glucosestatus = 'Worsened'
    context = {
            "heartratestatus":heartratestatus,
            "oxygenstatus":oxygenstatus,
            "glucosestatus":glucosestatus,
            "diastolicstatus":diastolicstatus,
            "systolicstatus":systolicstatus,
            "beforeheartrate":beforeheartrate,
            "beforeoxygenlevel":beforeoxygenlevel,              
            "afterheartrate":afterheartrate, 
            "afteroxygenlevel":afteroxygenlevel,
            "beforesystoliclevel":beforesystoliclevel,
            "beforediastoliclevel":beforediastoliclevel,
            "beforeglucoselevel":beforeglucoselevel,
            "afterdiastoliclevel":afterdiastoliclevel,
            "afterglucoselevel":afterglucoselevel,
            "aftersystoliclevel":aftersystoliclevel
            }
  
  

    return render(request, 'review.html',context)
