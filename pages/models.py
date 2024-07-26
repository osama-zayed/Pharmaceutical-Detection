from django.db import models
import uuid
from django.contrib.auth.models import User

    
def generate_unique_filename(instance, filename):
    extension = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{extension}'
    return f'Image/{unique_filename}'


class Imagegenuine(models.Model):
    Image = models.ImageField(upload_to=generate_unique_filename)

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username    

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField()
    comment = models.TextField()
    

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
class Medication(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=100)   
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_unique_filename, default='/image.jpg')

    
