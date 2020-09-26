import requests
import json
import pprint
import tokenEx

getSensorUrl = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/sensorData/get/"


def clientGetSensor(sensorUrl, name):
    headers = {"Authorization": tokenEx.token_h("p1")}

    params = {"wearerID": tokenEx.wearerId("w3"), "sensorName": name}
    response = requests.get(
        sensorUrl, headers=headers, params=params)
    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint.pprint(response_data)


if __name__ == "__main__":
    sensorUrl = getSensorUrl
    name = "tempHumid"
    clientGetSensor(sensorUrl, name)
