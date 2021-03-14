from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    full_name=models.CharField(max_length=18)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=30)
    address=models.CharField(max_length=20)

    def __str__(self):
        return self.full_name