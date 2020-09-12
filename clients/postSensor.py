import requests
import json

import tokenEx


def client():
    headers = {"Authorization": tokenEx.token_h("w2")}

    # wearerData/post
    data1 = {
        "temp": "17",
        "humid": "53",
        "heartRate": "47",
        "sound": "13",
        "stepCount": "2000",
    }

    data2 = {
        "temp": "24",
        "humid": "69",
        "heartRate": "89",
        "sound": "95",
        "stepCount": "3642",
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=data2)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
