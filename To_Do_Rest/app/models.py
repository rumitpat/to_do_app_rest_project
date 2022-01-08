from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TaskData(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    task_name =models.CharField(max_length=200)
    task_details =models.TextField()
    task_created_date =models.DateField(auto_now_add=True)
    test_created_time =models.TimeField(auto_now_add=True)
    task_end_date =models.DateField()
    task_end_time =models.TimeField()
    task_status =models.CharField(max_length =200,default=False)