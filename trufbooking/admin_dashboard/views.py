from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_log, logout as auth_logout
from django.http import HttpResponseForbidden
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.utils.timezone import now

from web.models import *

# Create your views here.


# system software 

def admin_dashbord(request):
    today = now().date()
    today_booking = Booking.objects.filter(created_at__date=today)
    today_revenue = today_booking.filter(status="BOOKED").aggregate(total=Sum("totel_price"))["total"] or 0

    context = {
        "total_users" : User.objects.count(),
        "total_owners" : User.objects.filter(is_agent = True).count(),
        "total_turfs" : Turf.objects.count(),
        "total_bookings" : Booking.objects.count(),
        "today_bookings" : today_booking.count(),
        "total_revenue" : today_revenue 
        }
 

    return render(request, "admin/admin_dashboard.html", context=context)



def today_bookings(request):
    today = now().date()
    tdy_bookings = Booking.objects.filter(booking_date= today)

    context = {
        "today_bookings" : tdy_bookings,
        "today" : today
    }

    return render(request, "admin/today-booking.html", context=context)


def user_list(request):
    user = User.objects.all().order_by("-id")
    return render(request, "admin/admin_user_list.html", {"users" : user})

def user_promte(request, user_id):
    user =  get_object_or_404(User, id =user_id)

    if not user.is_agent:
        user.is_agent = True
        user.save()
        
    return redirect("admin_dashboard:user_list")

def add_turf(request):
    pass
