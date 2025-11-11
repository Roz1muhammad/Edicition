from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('teacher/', views.oqtuvchi, name='oqituvchi'),
    path('student/', views.oquvchi, name='oqivchi'),
]
