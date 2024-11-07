# import random
# import requests
# import re
# from sms import send_sms
# from django.conf import settings

# def send_otp(phone_number):
#     # Generate a 6-digit OTP
#     otp = random.randint(100000, 999999)
    
#     # API endpoint
#     url = "https://textflow-sms-api.p.rapidapi.com/send-code"
    
#     # Message content
#     message = f'Your OTP code is {otp}'
    
#     # Textlocal request parameters
#     params = {
#         'apikey': settings.TEXTLOCAL_API_KEY,
#         'numbers': ,
#         'message': ,
#         'sender': settings.TEXTLOCAL_SENDER or 'TXTLCL',
#     }
    
#     payload = {
# 	"phone_number": phone_number,
# 	"service_name": "Your company name",
# 	"seconds": "60"
# }

#     headers = {
#         "x-rapidapi-key": "5a1064ef11msh19e06bd12bed4d2p15c92ajsnbdd3f946bbc9",
#         "x-rapidapi-host": "phonenumbervalidatefree.p.rapidapi.com"
#     }
#     # Send the request to API
#     response = requests.get(url, headers=headers, params=querystring)
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         print('OTP sent successfully')
#     else:
#         print('Failed to send OTP:', response.json())

#     # Return the OTP for further verification
#     return otp

# def format_phone_number(phone_number):
#     # Remove any non-numeric characters (e.g., spaces, hyphens, etc.)
#     phone_number = re.sub(r'\D', '', phone_number)
    
#     # Check if the number starts with '0' and replace it with '20' for international format
#     if phone_number.startswith('0'):
#         phone_number = '20' + phone_number[1:]
#     elif not phone_number.startswith('20'):
#         # If the number does not start with '20' or '0', assume it’s local and prepend '20'
#         phone_number = '20' + phone_number
    
#     # Now phone_number should be in the '201XXXXXXXXX' format
#     return phone_number


# def is_valid_phone_number(phone_number):
#     # Regular expression to match Egyptian phone numbers in international format
#     pattern = r'^0[1-9]\d{10}$'
    
#     return bool(re.match(pattern, phone_number))