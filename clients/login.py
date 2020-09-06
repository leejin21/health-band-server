import requests
import json
import pprint

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h()}

    # login
    credentials = {
        "username": "w3@gmail.com",
        "email": "w3@gmail.com",
        "password": "0000"
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/custom/login/", data=credentials)

    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint.pprint(response_data)


if __name__ == "__main__":
    client()
