from rest_framework import serializers 
from task_app.models import TASK
 
 
class TaskSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = TASK
        fields = ('id',
                  'profile',
                  'email',
                  'Mobile',
                  'Date_of_Birth',
                  'Skillset',
                  'price',
                  'discount_percent',
                  'discounted_price')