from django.urls import path
from web import views


app_name = "web"


urlpatterns = [
    path('',views.index , name='index'),
    path("single_turf/<int:id>/", views.single_turf, name="single_turf"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),

    path("turf_list/", views.turf_list, name="turf_list"),
    path("my_bookings/", views.my_bookings, name="my_bookings"),
    path("booking/<int:id>/", views.booking, name="booking"),
    path("delete_booking/<int:id>/", views.delete_booking, name="delete_booking"),
    path("cancel_booking/<int:id>/", views.cancel_booking, name="cancel_booking"),


    path("owner_dashboard/", views.owner_dashboard, name="owner_dashboard"),
    path("owner_turflist/", views.owner_turflist, name="owner_turflist"),
    path("owner_bookinglist/", views.owner_bookinglist, name="owner_bookinglist"),
    path("owner_bookinglist/", views.owner_bookinglist, name="owner_bookinglist"),
    path("owner_addturf/", views.owner_addturf, name="owner_addturf"),
    path("owner_editturf/<int:id>/", views.owner_editturf, name="owner_editturf"),
    path("owner_deleteturf/<int:id>/", views.owner_deleteturf, name="owner_deleteturf"),




 





    

    
]