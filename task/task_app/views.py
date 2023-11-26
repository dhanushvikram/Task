from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser 
from task_app.models import TASK
import boto3
from task_app.serializers import TaskSerializer
from rest_framework.decorators import api_view
from datetime import datetime
import task.settings
import re


session = boto3.Session(
                aws_access_key_id=task.settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=task.settings.AWS_SECRET_ACCESS_KEY,
                )

s3 = session.resource('s3')

x = datetime.now()
dt_strin = x.strftime("%Y-%m-%d%H-%M-%S")



  
 
@api_view(['GET', 'PUT', 'DELETE'])
def tasks(request, pk):
    try:
        profile=request.data['profile'] or None
        if profile:
            s3.Bucket(task.settings.AWS_STORAGE_BUCKET_NAME).put_object(Key='profile/%s' % dt_strin+profile.name, Body=profile)
            image= "https://"+task.settings.AWS_STORAGE_BUCKET_NAME+".s3."+task.settings.AWS_S3_REGION_NAME+".amazonaws.com/"+('curriculum_images'+'/'+dt_strin+str(profile.name))
        else:
            image = request.data['profile'] or None
      
        task_instance = TASK.objects.get(pk=pk)
        email = request.data['email'] or None
        local_part, domain = email.split('@')

        # Check if the domain is a personal email provider
        if domain in ['gmail.com', 'yahoo.com', 'outlook.com']:
            return JsonResponse({'message': 'Error: Personal email addresses are not allowed.'}, status=status.HTTP_404_NOT_FOUND)
            

        # Check if the local part contains any invalid characters
        if not re.match(r'^[a-zA-Z0-9-._]+$', local_part):
            return JsonResponse({'message': 'Error: Invalid email format.'}, status=status.HTTP_404_NOT_FOUND)
        Mobile = request.data['Mobile']
        # Check if country code is present

        # Check mobile number length
        if not len(Mobile) == 10:
            return JsonResponse({"Error: Mobile number should be 10 digits long."}, status=status.HTTP_404_NOT_FOUND)


        # Check for only numeric characters
        if not Mobile.isdigit():
            return JsonResponse({ "Error: Mobile number should contain only digits."}, status=status.HTTP_404_NOT_FOUND)
        Date_of_Birth = request.data['Date_of_Birth'] or None
        Skillset = request.data['Skillset'] or None
        price  = request.data['price'] or None
        discount_percent = request.data['discount_percent'] or None
        discounted_price =  int(price )- (int(price) * (int(discount_percent) / 100))


        values = {"profile":image,"email": email, "Mobile": Mobile,
                  "Date_of_Birth": Date_of_Birth,
                  "Skillset": Skillset, "price": price,
                  "discount_percent": discount_percent,
                  "discounted_price": discounted_price}
        task_serializer = TaskSerializer(instance=task_instance, data=values)

        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse({"message":"update successful"}, status=status.HTTP_200_OK)
        return JsonResponse(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except TASK.DoesNotExist:
        return JsonResponse({'message': 'The task does not exist'}, status=status.HTTP_404_NOT_FOUND)
    


