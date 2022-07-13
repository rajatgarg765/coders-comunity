from django.http import HttpResponse
from django.shortcuts import render, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.http import HttpResponse
# Create your views here.
def home(request):
    #allPost=Post.objects.all()
    allPost=Post.objects.all().order_by("-views")[:3]
    context={'allposts':allPost}
    #return HttpResponse("Hello this is home")
    return render(request,"home/home.html",context)

def contact(request):
    #return HttpResponse("Hello this is contatc")
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']

        if (len(name)<2 or len(email)<2 or len(phone)<10 or len(content)<2 ):
            messages.error(request,"Please fill the correct details")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your message has been sent successfully")
        #print("We are using post request")
    return render(request,"home/contact.html")

def about(request,authSlug):
    if authSlug==None:
        messages.success(request,"Welcome to About")
        return render(request,"home/contact.html")
    else:
        messages.success(request,"Welcome to About")
        authNames=Post.objects.filter(author=authSlug).first()
        authDesc=Post.objects.get(author=authSlug)
        print(authDesc)
        auth={"authNames":authNames,"authDesc":authDesc}
        return render(request,"home/about.html",auth)

def about1(request):
    messages.warning(request,"Currently in development mode")
    return render(request,"home/about.html")

def search(request):
    #allpost=Post.objects.all()
    query=request.GET['query']
    if len(query)>78:
        allpost=Post.objects.none()
    else:
        allpostTitle=Post.objects.filter(title__icontains=query)
        allpostContent=Post.objects.filter(content__icontains=query)
        allpost=allpostTitle.union(allpostContent)
    if allpost.count()==0:
        messages.warning(request,"No search results found")
    params={'allposts':allpost,'query':query}
    return render(request,"home/search.html",params)

#authentication apis

def handleSignup(request):
    if request.method=="POST":
        #get the post parameters
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #checks for error inputs
        if len(username)>15:
            messages.error(request, "Username must be less than 15 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username can only contain letters and numbers")
            return redirect('home')

        if pass1!=pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        #creating the user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, "Your ICoder account has been succesfully created")
        return redirect('home')

    else:
        return HttpResponse("404: NOT ALLOWED")

def handlelogin(request):
    if request.method=="POST":
        usernamelogin=request.POST['usernamelogin']
        loginpass=request.POST['loginpass']
        
        user=authenticate(username=usernamelogin, password=loginpass)

        if user is not None:
            login(request,user)
            messages.success(request," Successfully logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials , Please try again!")
            return redirect('home')
    else:
        return HttpResponse("404! NOT FOUND")

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully logged Out")
    return redirect('home')