# import requests
#
# # Define the URL and data
# url = "http://talaba.turin.uz/fish/api/v1/client-profile/"
# data = {
#     "username": "string",
#     "contact_number": "string",
#     "birthday": "2024-11-22",
#     "user_tg_id": "string"
# }
#
# # Send the POST request
# response = requests.post(url, json=data)
#
# # Print the response
# print(f"Status Code: {response.status_code}")
# print(f"Response Body: {response.text}")
# print(response.json())
import requests

def send_post_profile(data):
    url = "https://talaba.turin.uz/fish/api/v1/client-profile/"

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage

import requests

def send_post_request(data):
    url = "http://talaba.turin.uz/fish/api/v1/client-profile/"


    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# # Example usage
# data = {
#     "username": "string",
#     "contact_number": "string",
#     "birthday": "2024-11-22",
#     "user_tg_id": "string"
# }
#
# response = send_post_request(data)
#
# if response:
#     print(f"Status Code: {response.status_code}")
#     print(f"Response Body: {response.text}")
#
