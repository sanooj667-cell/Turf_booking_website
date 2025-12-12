from django.db import models

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