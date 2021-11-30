import requests
import random
from django.conf import settings
import urllib.request
import json

def send_otp_to_phone(mobile_no):

    try:
        otp = random.randint(1000, 9999)
            
        otp = str(otp)
        mobile_no = str(mobile_no)
        API_KEY = str(API_KEY)

        print("API_KEY: ", API_KEY)
        print("mobile_no: ", mobile_no)
        print("otp: ", otp)

        url = 'https://2factor.in/API/V1/f35586f7-51d5-11ec-b710-0200cd936042/SMS/' + mobile_no + '/' + otp
        response = requests.get(url)
        print("\nresponse: ", response, "\n")
            
        return otp

    except Exception as e:
        return None


