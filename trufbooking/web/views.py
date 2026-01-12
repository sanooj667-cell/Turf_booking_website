from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_log, logout as auth_logout
from django.http import HttpResponseForbidden
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required    


from .form import TurfForm
from .models import Sports_Category, Turf, Booking
from user.models import User

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    categories = Sports_Category.objects.all()
    turf = Turf.objects.all()[:3]
    context = {
        "categories" : categories,
        "turf" : turf
    }
    return render(request,"web/index.html", context=context)




def login(request):

    # 1️⃣ If form is submitted
    if request.method == "POST":

        # 2️⃣ Get values from form
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # 3️⃣ Role must be selected
        if not role:
            messages.error(request, "Please select a role")
            return redirect("web:login")

        # 4️⃣ Check email & password
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("web:login")

        # 5️⃣ Check role permission
        if role == "admin":
            if not user.is_manager:
                messages.error(request, "You are not an Admin")
                return redirect("web:login")

            # valid admin
            auth_log(request, user)
            return redirect("admin_dashboard:dashboard")

        elif role == "owner":
            if not user.is_agent:
                messages.error(request, "You are not an Owner")
                return redirect("web:login")

            # valid owner
            auth_log(request, user)
            return redirect("web:owner_dashboard")

        elif role == "user":
            if not user.is_customer:
                messages.error(request, "You are not a Customer")
                return redirect("web:login")

            # valid normal user
            auth_log(request, user)
            return redirect("web:index")

        # 6️⃣ If role value is something else
        else:
            messages.error(request, "Invalid role selected")
            return redirect("web:login")

    # 7️⃣ If GET request → show login page
    return render(request, "web/login.html")



def logout(request):
    auth_logout(request)
    return redirect("web:login")




def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "password do not match")
            return redirect("web:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exisits")
            return redirect("web:register")
        

        User.objects.create_user(
            email = email,
            password=password,
            first_name=name
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("web:login")

    return render(request, "web/register.html")



        










@login_required(login_url='/login/')
def turf_list(request):
    turfs = Turf.objects.all()

    context = {
        "turfs" : turfs
    }
    return render(request, "web/turfs.html", context=context)

def single_turf(request,id):
    turf = Turf.objects.get(id=id)
    context = {
        "turf" : turf
    }

    return render(request, "web/single_turf.html", context=context)



@login_required(login_url='/login/')
def booking(request, id):
    turf = get_object_or_404(Turf, id=id)
    if request.method == "POST":
        date = request.POST.get("date")
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")

        start_time = datetime.strptime(start,  "%H:%M")
        end_time = datetime.strptime(end,  "%H:%M")

        if end_time <= start_time:
            messages.error(request, "End time must be greater than start time")
            return redirect("web:booking",id=id)

        duaration = end_time - start_time
        hours = duaration.seconds / 3600

        totel_price = int(hours*turf.price)

        conflict = Booking.objects.filter(
            turf = turf,
            booking_date = date,
            start_time = start_time,
            end_time = end_time).exclude(status='CANCELLED').exists()
        
        if conflict:
            messages.error(request, "This time slot is already booked.")
            return redirect("web:booking", id=id)

        

        Booking.objects.create(
            user = request.user,
            turf = turf,
            booking_date = date,
            start_time = start,
            end_time = end,
            totel_price = totel_price,
        )
        

        return redirect("web:my_bookings")
    return render(request, "web/booking.html", {"turf": turf})


@login_required(login_url='/login/')
def my_bookings(request):
    bookings = Booking.objects.filter(user = request.user)
    return render(request, "web/my_bookings.html", {"bookings":bookings})

@login_required(login_url='/login/')
def delete_booking(request,id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    booking.delete()
    return redirect( "web:my_bookings")

@login_required(login_url='/login/')
def cancel_booking(request,id):
    booking = get_object_or_404(Booking, id=id)
    booking.status ="CANCELLED"
    booking.save()
    return redirect( "web:my_bookings")


 
def owner_dashboard(request):
    if not request.user.is_agent:
        return HttpResponseForbidden("You are not allowed to access this page")
    turfs = Turf.objects.filter(owner=request.user)
    booking = Booking.objects.filter(turf__owner= request.user)
    totel_revenue = (
                    booking
                    .filter(status="BOOKED")
                    .aggregate(totel=Sum("totel_price"))
                )["totel"] or 0

    context = {
        "totel_turfs" : turfs.count(),
        "totel_bookings" : booking.count(),
        "confirmed_bookings" : booking.filter(status="BOOKED").count(),
        "cancelled_bookings" : booking.filter(status="CANCELLED").count(),
        "totel_revenue":totel_revenue,
    }
    
    return render(request,"owner/dashbord.html", context=context)


def owner_turflist(request):
    if not request.user.is_agent:
        return HttpResponseForbidden("You are not allowed to access this page")
    
        
    turfs = Turf.objects.filter(owner = request.user)
    context = {
        "turfs" : turfs
    }
    return render(request, 'owner/owner_turflist.html' , context=context)


def owner_bookinglist(request):
    if not request.user.is_agent:
        return HttpResponseForbidden("You are not allowed to access this page")
    
    bookings = Booking.objects.filter(turf__owner = request.user)
    context={
        "bookings" : bookings
    }
    
    return render(request, 'owner/owner_bookinglist.html' , context=context)



def owner_addturf(request):
    if not request.user.is_agent:
        return HttpResponseForbidden("You are not allowed to access this page")
    

    if request.method == "POST":
        form = TurfForm(request.POST, request.FILES,)
        if form.is_valid(): 
            turf = form.save(commit=False)
            turf.owner = request.user
            turf.save()
            return redirect("web:owner_turflist")
    else:
        form = TurfForm()
        

    return render(request, "owner/add_turf.html", {"form": form})        




def owner_editturf(request,id):
    if not request.user.is_agent:
        return HttpResponseForbidden("You are not allowed to access this page")
    
    instance = get_object_or_404(Turf, id=id, owner=request.user)


    if request.method == "POST":
        form = TurfForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("web:owner_turflist")
    else:
        form = TurfForm(instance=instance)


    return render (request, "owner/add_turf.html", {"form": form})


def owner_deleteturf(request, id):
    instance = get_object_or_404(Turf, id=id)
    instance.delete
    return redirect("web:owner_dashboard")


            















































    















