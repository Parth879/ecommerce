from django.urls import path
from store.views import *


urlpatterns = [
    
    path('',store,name='store'),

    path('<category_slug>/',store,name='store'),


]