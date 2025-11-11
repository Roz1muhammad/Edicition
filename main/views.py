from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Noto‘g‘ri foydalanuvchi nomi yoki parol!")
    return render(request, 'login.html')

def oqtuvchi(request):
    return render(request, "oqituvchi_page.html")

def oquvchi(request):
    return render(request, "oquvchi_page.html")