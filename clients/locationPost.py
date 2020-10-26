import requests
import json

import tokenEx


def client_post():
    headers = {"Authorization": tokenEx.token_h("w1")}

    # wearerData/post

    data2 = {
        "latitude": "37.50423",
        "longitude": "127.0007899"
    }

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerLocation/post/", headers=headers, data=data2)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client_post()
