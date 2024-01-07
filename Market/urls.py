
from django.contrib import admin
from django.urls import path
from Market.views import market_analysis,Home,Api_search

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', Home),
    path('api/<str:search>/', Api_search),
    path('analysis/', market_analysis),
]
