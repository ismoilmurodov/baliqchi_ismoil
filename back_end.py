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


def send_post_request(data):
    url = "http://talaba.turin.uz/fish/api/v1/client-profile/"

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_categories():
    url = "http://talaba.turin.uz/fish/api/v1/categories/"

    try:
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the JSON data from the response
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Function to fetch products from the API based on the category
async def fetch_products_by_category(category: str):
    url = f"http://talaba.turin.uz/fish/api/v1/categories/{category}/products/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('products', [])
    else:
        return []  # Return an empty list if the API request fails


async def fetch_product_details(category: str, product_name: str):
    url = f"http://talaba.turin.uz/fish/api/v1/categories/{category}/{product_name}/"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('product', {})
    else:
        return None  # Return None if the API request fails
