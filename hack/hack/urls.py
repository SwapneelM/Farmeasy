"""hack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^sms',views.sms),
	url(r'^getlocation/(\d+)',views.get_location),
	url(r'^registerfarmer',views.register_farmer),
	url(r'^inputlocation/',views.enter_location_data),
	url(r'^stresslocation/(\d+)/(\d+)',views.stress_location),
	url(r'^vegetationcloud/(\d+)',views.vegetation_outlier),
	url(r'^$', views.index), 
	url(r'^curve/(\d+)$', views.curve),
	url(r'^display_curve/(\d+)', views.display_curve),
	url(r'^findpeak/(\d+)', views.find_peak),
	url(r'^recommend/(\d+)', views.recommend),
	url(r'^ahmedabad/', views.ahmedabad),
	url(r'^jamnagar/', views.jamnagar),
	url(r'^wheat/', views.wheat),
	url(r'^bajra/', views.bajra),
	url(r'^home/(\d+)', views.home),
	url(r'^information', views.information),
]
