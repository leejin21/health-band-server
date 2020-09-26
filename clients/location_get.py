import requests
import json
import pprint
import tokenEx

url = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerLocation/get/"


def client(url):
    headers = {"Authorization": tokenEx.token_h("p1")}

    params = {"wearerID": tokenEx.wearerId("w3")}
    response = requests.get(
        url, headers=headers, params=params)
    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint.pprint(response_data)


if __name__ == "__main__":
    client(url)
