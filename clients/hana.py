import requests
import json

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h()}

    # login
    # credentials = {
    #     "username": "w4@gmail.com",
    #     "email": "w4@gmail.com",
    #     "password": "0000"
    # }

    # response = requests.post(
    #     "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/custom/login/", data=credentials)

    # linkedUsers/post

    # data = {
    #     "wearer": "w4@gmail.com",
    #     "protector": "p2@gmail.com"
    # }

    # wearerData/post
    data = {
        "tempHumid": "50",
        "gyro": "80",
        "accel": "20",
        "heartRate": "30",
        "sound": "30",
        "vibrate": "30",
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=data)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
