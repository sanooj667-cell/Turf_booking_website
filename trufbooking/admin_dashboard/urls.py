from django.urls import path
from . import views

app_name = "admin_dashboard"

urlpatterns = [
    path("", views.admin_dashbord, name="dashboard"),
    path("today_bookings/", views.today_bookings, name="today_bookings"),
    path("user_list/", views.user_list, name="user_list"),
    path("user_promte/<int:user_id>/", views.user_promte, name="user_promte"),
]
