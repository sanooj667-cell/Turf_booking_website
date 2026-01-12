from django.db import models
from user.models import User

# Create your models here.

class Sports_Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)

    class Meta:
        ordering = ['-id']
        verbose_name = "Sports Category"
        verbose_name_plural = "Sports Categories"

    def __str__(self):
        return self.name
    


class Turf(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="turfs")
    category = models.ForeignKey(Sports_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)    
    price = models.IntegerField()
    image = models.ImageField(upload_to='turfs/')
    description = models.CharField(max_length=500)

    class Meta:
        ordering = ['-id']
        verbose_name = "Turf"
        verbose_name_plural = "Turfs"
        
    def __str__(self):
        return self.name
    


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)

    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    totel_price = models.IntegerField()

    status = models.CharField(max_length=20, choices=[("BOOKED", "Booked"),
                                                      ("CANCELLED", "Cancelled"),
                                                      ("COMPLETED", "Completed"),],default="BOOKED")
    
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.turf.name}"    