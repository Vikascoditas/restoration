from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseNotFound,HttpResponse
from functions.function import handle_uploaded_file, restore
from accounts.forms import FileForm

def handle_invalid_url(request, path):
    return HttpResponseNotFound("Enter a valid URL.")

@login_required
def home_view(request):
    if request.method == 'POST':  
        student = FileForm(request.POST, request.FILES)
        if student.is_valid():  
            print(request.FILES['file'])
            handle_uploaded_file(request.FILES['file'])  
            restore(request.FILES['file'])
            return render(request, "accounts/success.html", {})  
        else:  
            student = FileForm()  
    student = FileForm     
    return render(request, "accounts/home.html", {'form': student})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')  # Redirect to home if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not (user.username == 'Coditas' or user.username == 'vikas'):
                return HttpResponse("Authentication failed. Access denied.")

            login(request, user)
            return redirect('/home')
    else:
        form = AuthenticationForm(request)
    context = {"form": form}        
    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/login")

    return render(request, 'accounts/logout.html', {})
