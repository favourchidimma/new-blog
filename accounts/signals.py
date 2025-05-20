from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
import random
from django.utils import timezone
from .models import*
import requests


def generate_otp():

    otp = random.randint(000000, 999999)


    return otp



User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance,created,**kwargs):

    if created:

        if instance.role in ('app_admin', 'root_admin', 'user'):

            instance.is_active = False

            instance.save()

            otp = generate_otp()
            print(otp)

            expiry_date = timezone.now() + timezone.timedelta(minutes=3)

            OTP.objects.create(
                otp = otp,
                expiry_date = expiry_date,
                user = instance

            )

        url = "https://api.useplunk.com/v1/track"
        header = {
            "Authorization": "Bearer sk_334d8f7b167c03fefbee578f94601ec40d39d8bedaf3c698",
            "Content-Type": "application/json"
        }

        data = {
            "email": instance.email,
            "event": "welcome",
            "data": {
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "otp": str(otp)
            }
        }

        response = requests.post(
            url=url,
            headers=header,
            json=data
        )

        print(response.json())





