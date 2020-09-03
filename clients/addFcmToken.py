import requests
import json
import pprint

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h()}

    # login
    credentials = {
        "username": "w3@gmail.com",
        "fcm_token": "hellp"
    }

    response = requests.put(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/user/changeFcmToken/", data=credentials, headers=headers)

    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint.pprint(response_data)


if __name__ == "__main__":
    client()
