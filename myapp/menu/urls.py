from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
]