from django.contrib import admin
from django.urls import path
from simulation.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', index,name='create'),
    path('execute/', index, name='execute'),
]
