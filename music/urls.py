from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
   
 
  
    url(r'^create_trip/$', views.create_trip, name='create_trip'),
   
    url(r'^(?P<trip_id>[0-9]+)/favorite_trip/$', views.favorite_trip, name='favorite_trip'),
    url(r'^(?P<trip_id>[0-9]+)/delete_trip/$', views.delete_trip, name='delete_trip'),
]
