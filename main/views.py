from django.shortcuts import render,redirect
from .models import *
# Create your views here.
import requests
import json
import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='signup')
def dates (request ):
    dates = [str(datetime.date.today() + datetime.timedelta(i)) for i in range(5)]
    # print(dates)
    return render(request,"datesBs.html",{"dates":dates})
    
    
# @login_required(login_url='signup')
def home (request ):
    return render(request,"indexBs.html",{})

@login_required(login_url='signup')
def rutesView (request ,date):
    rutesList= rutes.objects.filter(bus_date=date)
    return render(request,"rutesBS.html",{'date':date,"rutes":rutesList})

# @login_required(login_url='signup')
# def signup (request ):
#     return render(request,"signupBs.html",{})

@login_required(login_url='signup')
def weather(request ,rute):
    busStops = rutes.objects.filter(id=rute)
    bus_date = rutes.objects.filter(id = rute ).values_list("bus_date")[0][0] 
    d =bus_date.strftime('%Y-%m-%d')
    # print(busStops)
    cityNameTemp =[]
    for j in busStops[0].bus_rutes.values():
        # print(j)
        url = r"https://api.open-meteo.com/v1/dwd-icon?latitude="+str(j["latitude"])+"&longitude="+str(j["longitude"])+r"&current_weather=true&daily=apparent_temperature_max,apparent_temperature_min,rain_sum,windspeed_10m_max,weathercode&temperature_unit=fahrenheit&forecast_days=3&start_date="+d+r"&end_date="+d+r"&timezone=auto"
        resp = requests.get(url)
        vals = json.loads(resp.text)
        # print(vals)
        data ={}
        data["apparent_temperature_max"] = vals["daily"]["apparent_temperature_max"][0]
        data["apparent_temperature_min"] = vals["daily"]["apparent_temperature_min"][0]
        data["rain_sum"] = vals["daily"]["rain_sum"][0]*100
        data["windspeed_10m_max"] = vals["daily"]["windspeed_10m_max"][0]
        data["city_name"] = j["city_name"]
        code = vals["daily"]["weathercode"][0] 
        # if code == 0 :
        #     data["img_url"] = r"https://i.gifer.com/origin/45/454ba38b4ce5b3fdc8796ed710769e69.gif"
        # elif code == 1 or code == 2 or code == 3 :
        #     data["img_url"] = r"https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmExZTExZGU3ZTExMjJlYzUyZmY0YmZmYjViMWVkNDkwMTAzOGNmNiZjdD1n/aQ7kognlRPDzi/giphy.gif"
        # elif code == 45 or code == 48 :
        #     data["img_url"] = r"https://i.pinimg.com/originals/4f/9d/8f/4f9d8f32bf3103a9c8fbbce7a7075c09.gif"
        # elif code == 51 or code == 53 or code == 55 or code == 56 or code == 57:
        #     data["img_url"] = r"https://giffiles.alphacoders.com/105/105296.gif"
        # elif code == 61 or code == 63 or code == 65 or code == 66 or code == 67 :
        #     data["img_url"]= r"https://i.gifer.com/GYlk.gif"
        # elif code == 71 or code == 73 or code == 75 or code == 77 or code == 80 or code == 81 or code == 82 :
        #     data["img_url"]= r"https://i.gifer.com/Dv9E.gif"
        # else :
        #     data["img_url"]= r"https://thumbs.gfycat.com/HarmfulWaryHarborporpoise-max-1mb.gif"
        # print(data)
        cityNameTemp.append(data)
    return render(request,"weatherBS.html",{"cityNameTemp":cityNameTemp,"bus_date":bus_date})

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
 
def signup(request):
 
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('home')
         
        else:
            return render(request,'signupBs.html',{'form':form})
     
    else:
        form = UserCreationForm()
        return render(request,'signupBs.html',{'form':form})
    
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
 
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            form = AuthenticationForm()
            return render(request,'signupBs.html',{'form':form})
    else:
        form = AuthenticationForm()
        return render(request, 'signupBs.html', {'form':form})
    
@login_required(login_url="signup")
def signout(request):
    logout(request)
    return redirect('home')