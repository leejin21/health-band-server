import requests
import json
import pprint

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h('abc')}

    # login
    credentials = {
        "username": "abc@gmail.com",
        "fcm_token": "abc-token"
    }

    response = requests.put(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/user/changeFcmToken/", data=credentials, headers=headers)

    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint.pprint(response_data)


if __name__ == "__main__":
    client()
