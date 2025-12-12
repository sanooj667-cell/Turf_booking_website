from django.urls import path
from web import views


app_name = "web"


urlpatterns = [
    path('',views.index , name='index'),
    path("single_turf/<int:id>/", views.single_turf, name="single_turf"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),

    
]