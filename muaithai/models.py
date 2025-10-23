from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Fighter_Details(models.Model):
    Name = models.CharField(max_length = 48)
    Weight_class = models.CharField(max_length = 48)
    Age = models.PositiveSmallIntegerField(default=18)
    Prof_record = models.CharField(max_length=50,default=0)
    p4p_rank = models.IntegerField(default=99, null = True)
    Image = models.ImageField(upload_to='fighters/', blank=True, null=True)
    # created_at = models.DateField(default=timezone.now)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Name + self.Weight_class + str(self.created_at)
    
    #tells me where the page has to redirect after submiting form 
    def get_absolute_url(self):
        return reverse ('homepage')


class Carousel(models.Model):
    title = models.CharField(max_length = 90)
    description = models.CharField(max_length = 240)
    image = models.ImageField(upload_to='fighters/', blank= True, null= True) 





