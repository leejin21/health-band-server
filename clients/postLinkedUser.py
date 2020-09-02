import requests
import json

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h()}

    # linkedUsers/post

    data = {
        "wearer": "w4@gmail.com",
        "protector": "p2@gmail.com"
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/linkedUser/post/", headers=headers, data=data)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
