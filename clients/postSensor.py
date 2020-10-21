import requests
import json

import tokenEx

other1 = {
    "temp": "17",
    "humid": "53",
    "heartRate": "47",
}

other2 = {
    "temp": "24",
    "humid": "69",
    "heartRate": "89",
}

meter1 = {
    "meter": "500"
}

meter2 = {
    "meter": "1000"
}
meter3 = {
    "meter": "3000"
}


def post_other(user, data):
    headers = {"Authorization": tokenEx.token_h(user)}

    # wearerData/post

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=data)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


def post_meter(user, data):
    headers = {"Authorization": tokenEx.token_h(user)}

    # wearerMeter/post/

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerMeter/post/", headers=headers, data=data)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    # post_other("w3", other1)
    post_meter("w3", meter3)
