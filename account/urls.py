from django.urls import path
from account.views import *

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('activate/<uid64>/<token>/',activate,name='activate'),
    path('logout/',logout,name="logout"),
    path('UserDashboard/',UserDashboard,name='UserDashboard'),
]