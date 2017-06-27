from django.conf.urls import url
#from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$', views.travels),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^addtravel$', views.addtravel),
    url(r'^addtrip$', views.addtrip),
    url(r'^travels/destination/(?P<trip_id>\d+)$', views.showtrip),
    url(r'^travels/jointrip/(?P<trip_id>\d+)$', views.jointrip),
]

