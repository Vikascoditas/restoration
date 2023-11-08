from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseNotFound, HttpResponse
from functions.function import handle_uploaded_file, restore, process_excel_and_create_text_file
from accounts.forms import FileForm
import os
from django.core.files.uploadedfile import InMemoryUploadedFile


def handle_invalid_url(request, path):
    return HttpResponseNotFound("Enter a valid URL.")


def home_view(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            input_xlsx_file = form.cleaned_data['file']
            script_directory = os.path.dirname(os.path.abspath(__file__))
            output_text_file_path = process_excel_and_create_text_file(input_xlsx_file, script_directory)
            if output_text_file_path:
                restore(output_text_file_path)
                return render(request, "accounts/success.html", {})
    else:
        form = FileForm()

    return render(request, "accounts/home.html", {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.isvalid():
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
