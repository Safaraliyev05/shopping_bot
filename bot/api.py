import requests

BASE_URL = 'http://127.0.0.1:8000'


def create_user(full_name, phone_number):
    url = f"{BASE_URL}/users/create/"
    payload = {
        "full_name": full_name,
        "phone_number": phone_number
    }

    response = requests.post(url=url, json=payload)
    print(response.status_code)
    print(response.json())

# create_user("sardor", '998990708605')
