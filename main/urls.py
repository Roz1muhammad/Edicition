from django.urls import path
from .views import login_view,admin_dashboard,teacher_dashboard,student_dashboard


urlpatterns = [
    path('', login_view, name='main'),
    path('sayit_admin/', admin_dashboard, name='admin_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),
]
