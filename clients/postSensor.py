import requests
import json

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h()}

    # wearerData/post
    data1 = {
        "temp": "10",
        "humid": "50",
        "heartRate": "100",
        "sound": "20",
        "stepCount": "1000",
    }

    data2 = {
        "temp": "30",
        "humid": "70",
        "heartRate": "80",
        "sound": "40",
        "stepCount": "2000",
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=data2)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
