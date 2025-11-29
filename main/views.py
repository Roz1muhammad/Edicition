
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models.auth import User
from .models.grups import Course, Group, GroupStudent, Interested
from django.contrib.auth.decorators import login_required
from main.forms.forms1 import AdminCreateUserForm, AdminCreateCourseForm, AdminCreateGroupForm

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')


        user = authenticate(request, username=phone, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # To‘g‘ri yo‘l: ut field orqali tekshirish
                if user.ut == 1:
                    return redirect('admin_dashboard')
                elif user.ut == 2:
                    return redirect('teacher_dashboard')
                elif user.ut == 3:
                    return redirect('student_dashboard')
            else:
                messages.error(request, "Hisobingiz faol emas!")
        else:
            messages.error(request, "Noto‘g‘ri telefon raqami yoki parol!")

    return render(request, 'login.html')


# -------------------- Admin ----------------------------


@login_required
def admin_dashboard(request):
    if request.user.ut != 1:
        return redirect('main')

    ctx = {}

    all_groups = Group.objects.all()
    groups_with_counts = []
    for group in all_groups:
        student_count = GroupStudent.objects.filter(group=group).count()
        groups_with_counts.append({
            "group": group,
            "student_count": student_count
        })

    all_courses = Course.objects.all()
    courses_with_counts = []
    for course in all_courses:
        group_count = Group.objects.filter(course=course).count()
        courses_with_counts.append({
            "course": course,
            "group_count": group_count
        })

    interested_all = Interested.objects.all()
    interested_count = interested_all.count()


    total_students = User.objects.filter(ut=3).count()

    ctx.update({
        "groups_with_counts": groups_with_counts,
        "courses_with_counts": courses_with_counts,
        "interested_all": interested_all,
        "interested_count": interested_count,

        "total_students": total_students,
    })

    if request.method == 'POST':
        if 'create_user' in request.POST:
            user_form = AdminCreateUserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('admin_dashboard')
        else:
            user_form = AdminCreateUserForm()

        if 'create_course' in request.POST:
            course_form = AdminCreateCourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect('admin_dashboard')
        else:
            course_form = AdminCreateCourseForm()

        if 'create_group' in request.POST:
            group_form = AdminCreateGroupForm(request.POST)
            if group_form.is_valid():
                group_form.save()
                return redirect('admin_dashboard')
        else:
            group_form = AdminCreateGroupForm()
    else:
        user_form = AdminCreateUserForm()
        course_form = AdminCreateCourseForm()
        group_form = AdminCreateGroupForm()

    ctx.update({
        "user_form": user_form,
        "course_form": course_form,
        "group_form": group_form
    })

    return render(request, "base.html", ctx)

# -------------------- Oqituvchi ----------------------------


@login_required
def teacher_dashboard(request):
    if request.user.ut != 2:
        return redirect('main')

    ctx = {}
    teacher_courses = Course.objects.filter(mentor=request.user)
    teacher_groups = Group.objects.filter(course__in=teacher_courses)
    groups_with_students = []


    for group in teacher_groups:
        students_qs = GroupStudent.objects.filter(group=group, student__ut=3).select_related('student')
        students = [gs.student for gs in students_qs]
        groups_with_students.append({
            "group": group,
            "students": students,
            "student_count": len(students)
        })

    ctx["groups_with_students"] = groups_with_students
    return render(request, "base.html", ctx)

# -------------------- Oquvchi ----------------------------

@login_required
def student_dashboard(request):
    if request.user.ut != 3:
        return redirect('main')

    ctx = {}
    student_groups = Group.objects.filter(groupstudent__student=request.user)
    ctx["student_groups"] = student_groups
    return render(request, "base.html", ctx)