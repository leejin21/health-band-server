import requests
import json


def client():
    # login
    # credentials = {
    #     "username": "w4@gmail.com",
    #     "email": "w4@gmail.com",
    #     "password": "0000"
    # }

    # response = requests.post(
    #     "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/custom/login/", data=credentials)

    # linkedUsers/post
    token_h = "Token 3d27b7ea469d77cc51039650573df7dd0a344ffa"
    headers = {"Authorization": token_h}
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
