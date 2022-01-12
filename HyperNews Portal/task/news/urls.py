from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view),
    path('create/', views.create_view),
    path('<int:link>/', views.link_view),
]
