from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Post
# Create your views here.
def index(request):
    return render(request, "RegLog.html")

def success(request):
    print(request.POST)
    Errors = User.objects.regVal(request.POST)
    if len(Errors)> 0:
        for key, value in Errors.items():
            messages.error(request, value)
        return redirect("/")


    newUser = User.objects.create(name = request.POST['form_name'], email = request.POST['form_email'], password = request.POST['form_pw'])

    request.session["logInID"] = newUser.id 
    return redirect("/travels")

def travels(request):
    print("!!!")
    print(User.objects.all())
    print(Post.objects.all())
    if "logInID" not in request.session:
        return redirect("/")
    logInUser = User.objects.get(id = request.session["logInID"])
    allUser : User.objects.all()
    context = {
        "allPost" : Post.objects.all(),
        "logInUser" : logInUser,
        "userTrips" : Post.objects.filter(fav = User.objects.get(id = request.session["logInID"])),
        "nonuserTrips": Post.objects.exclude(fav = User.objects.get(id = request.session["logInID"]))
    }
    
    return render(request, "travels.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    print(request.POST)
    Errors = User.objects.logVal(request.POST)
    if len(Errors)> 0:
        for key, value in Errors.items():
            messages.error(request, value)
        return redirect("/")
    filter = User.objects.filter(email = request.POST["form_email"])
    request.session["logInID"] = filter[0].id

    return redirect("/travels")

def add(request):
    print("Its in the Terminal")
    print(request.POST)
    print("*******")
    print(Post.objects.all())
    print("*******")
    context = {
        "allDesti" : Post.objects.all(),
        
    }

    return render(request, "addPlan.html", context)

def uploadTrip(request):
    print(request.POST)
    Errors = Post.objects.postVal(request.POST)
    if len(Errors)> 0:
        for key, value in Errors.items():
            messages.error(request, value)
        return redirect("/travels/add")
    newTrip = Post.objects.create(desti = request.POST['desti'], plan = request.POST['desc'], startDate = request.POST['from'], endDate = request.POST['to'],
    user = User.objects.get(id =request.session["logInID"]))
    return redirect("/travels")

def tripID(request, tripID):
    #tripID = Post.objects.get(id = tripID)
    print("!!!!!!!")
    print(request.POST)
    context = {
        "tripInfo" : Post.objects.get(id = tripID),
        "allPost" : Post.objects.all()
        
    }

    return render(request, "desti.html", context)

def join(request, tripID):
    logInUser = User.objects.get(id = request.session["logInID"])
    joinTrip = Post.objects.get(id = tripID)
    joinTrip.fav.add(logInUser)
    return redirect("/travels")
