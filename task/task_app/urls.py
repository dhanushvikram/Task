from django.urls import include, re_path 
from task_app import views 
 
urlpatterns = [ 
    re_path(r'^task/(?P<pk>[0-9]+)$', views.tasks),
]