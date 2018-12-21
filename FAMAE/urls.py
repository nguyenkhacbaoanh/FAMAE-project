"""FAMAE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from SavingWater import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SavingWater.urls')),
    path('consommation/', views.consommation, name='consommation'),
    path('limited-ressource/', views.limited_ressource, name='limited-ressource'),
    path('alimentation/', views.alimentation, name='alimentation'),
    path('water-stress/', views.water_stress, name='water_stress'),
    path('ws_a_1/', views.ws_a_1, name='ws_a_1'),
    path('ws_a_2/', views.ws_a_2, name='ws_a_2'),
    path('ws_a_3/', views.ws_a_3, name='ws_a_3'),
    path('ws_a_4/', views.ws_a_4, name='ws_a_4'),
    path('pie-chart-1/', views.pie_chart, name='piechart'),
    path('bar-chart-1/', views.bar_chart_water_per_cap, name='barchart1'),
    path('bar-chart-2/', views.bar_chart_water_municipal, name='barchart2'),
    path('bar-chart-3/', views.bar_chart_water_com_renou, name='barchart3'),
    path('map-1/', views.map_irrigation_water, name='map1'),
    # path('datanetwork/', views.DataNet, name='datanetwork'),
    path('alementaire/', views.DataAli, name='alimentaire'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)