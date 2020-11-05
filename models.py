from django.db import models
from datetime import date

# Create your models here.

class UserManager(models.Manager):
    def regVal(self, requestPOST):
        errors = {}
        #ClassName.objects.filter(field1="value for field1", etc.) - gets any records matching the query provided
        filter = User.objects.filter(email = requestPOST["form_email"])
        print(filter)
        if len(requestPOST["form_name"]) < 3:
            errors["name"] = "Your name is required and must be at least 3 characters!"
        if len(requestPOST["form_email"]) < 3:
            errors["fEmailReq"] = "Username is required must be at least 3 characters!"
        if len(filter) > 0:
            errors["emailtaken"] = "This Username is taken!"
        if len(requestPOST["form_pw"]) < 8:
            errors["fPwordReq"] = "Password is required and must be at least 8 characters!"
        if requestPOST["form_cpw"] != requestPOST["form_pw"]:
            errors["fCwordReq"] = "Confirm Password must match!"
        return errors

    def logVal(self, requestPOST):
        errors = {}
        filter = User.objects.filter(email = requestPOST["form_email"])
        if len(requestPOST["form_email"]) == 0:
            errors["fEmailReq"] = "Email is required to login!"
        if len(requestPOST["form_pw"]) == 0:
            errors["fPwordReq"] = "Password is required to login!"
        elif len(filter) == 0:
            errors["emailNotFound"] = "Email not found. Please register first!"
        else: 
            print("Email Found!")
            if filter[0].password != requestPOST["form_pw"]:
                errors["PwordMatch"] = "Incorrect password"        
        return errors


class PostManager(models.Manager):
    def postVal(self, requestPOST):
        errors = {}
        if len(requestPOST['desti']) < 1:
            errors['destiNamelength'] = "Destination can not be empty."
        if len(requestPOST['desc']) < 1:
            errors['descMesslength'] = "Description can not be empty."
        if requestPOST['from'] < date.today().strftime("%Y-%m-%d"):
            errors['notToday'] = "Dates have to be future dated."
        elif requestPOST['to'] < date.today().strftime("%Y-%m-%d"):
            errors['futureDate'] = "Can not travel before 'Date From'."
        return errors




class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Post(models.Model):
    desti = models.CharField(max_length = 255)
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(auto_now_add=True)
    plan = models.CharField(max_length = 45)
    user = models.ForeignKey(User, related_name="dest", on_delete = models.CASCADE)
    fav = models.ManyToManyField(User, related_name= "trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()
