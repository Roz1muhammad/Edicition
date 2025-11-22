from django.urls import path
from .views import a_views,s_views

urlpatterns = [
    path('', a_views.info_view, name='info'),
    path('login/', a_views.login_view, name='login_view'),
    path('logout/', a_views.logout_view, name='logout'),
    path('oqituvchi/<int:user_id>/', a_views.teacher_view, name='oqituvchi'),
    path('oquvchi/<int:user_id>/', s_views.student_view, name='oqivchi'),
    path('adm1n/<int:user_id>/', a_views.adm1n, name='adm1n'),

]

