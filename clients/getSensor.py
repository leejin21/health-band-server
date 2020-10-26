import requests
import json
import pprint
import tokenEx


def clientGetSensor(sensorUrl):
    headers = {"Authorization": tokenEx.token_h("p1")}

    params = {"wearerID": tokenEx.wearerId("w1")}
    response = requests.get(
        sensorUrl, headers=headers, params=params)
    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint.pprint(response_data)


if __name__ == "__main__":
    url = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/get/"
    clientGetSensor(url)
