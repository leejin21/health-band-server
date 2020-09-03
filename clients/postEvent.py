import requests
import json

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h()}

    # wearerData/post

    data2 = {
        "fallEvent": "T",
        "heartEvent": "F",
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerEvent/post/", headers=headers, data=data2)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
