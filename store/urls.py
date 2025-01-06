from django.urls import path
from store.views import *


urlpatterns = [
    
    path('',store,name='store'),

    path('<category_slug>/',store,name='product_by_category'),

    path('<category_slug>/<product_slug>/',product_details,name='product_details'),

    path('search',search,name="search"),

]