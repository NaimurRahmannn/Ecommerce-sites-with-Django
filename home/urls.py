from django.urls import path
from home.views import index, contact
urlpatterns = [
     path('',index, name="index"),
     path('contact/', contact, name="contact"),
]