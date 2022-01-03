from django.urls import path
from photos import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('gallery/', views.gallery , name='gallery'),
    path('add/', views.addPhoto , name='add'),
    path('view/<str:pk>/', views.viewPhoto , name='photo'),
    path('', views.CustomisedLogin.as_view() , name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login') , name='logout'),
    path('register/', views.RegisterPage.as_view() , name='register'),

  
]
