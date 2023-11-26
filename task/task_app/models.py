from django.db import models

# Create your models here.
class TASK(models.Model):
  id = models.AutoField(
    primary_key=True
  )

  profile = models.TextField(
    max_length=1000,
    null=True,
    blank=False
  )
  email = models.TextField(
    max_length=100,
    null=True,
    blank=False
  )
  Mobile = models.TextField(
    max_length=1000,
    null=True,
    blank=False
  )  
  Degree_Department = models.IntegerField(
    null=True,
    blank=False
  )  
  Date_of_Birth = models.DateField(
    null=True,
    blank=False
  )

  Skillset = models.IntegerField(
    null=True,
    blank=False
  ) 

  price = models.FloatField(
    null=True,
    blank=False
  )  

  discount_percent = models.IntegerField(
    null=True,
    blank=False
  ) 

  discounted_price = models.FloatField(
    null=True,
    blank=False
  )

  class Meta:
    db_table = 'Task'