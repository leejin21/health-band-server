import requests
import json
import pprint
import sys

import tokenEx

getSensorUrl = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/sensorData/get/"


def clientGetSensor(sensorUrl, namelist, prot, wear):
    headers = {"Authorization": tokenEx.token_h(prot)}
    for name in namelist:
        params = {"wearerID": tokenEx.wearerId(wear), "sensorName": name}
        response = requests.get(
            sensorUrl, headers=headers, params=params)
        print("Status Code:", response.status_code)
        response_data = response.json()
        pprint.pprint(response_data)


if __name__ == "__main__":
    sensorUrl = getSensorUrl
    namelist = ["tempHumid", "heartRate", "stepCount"]
    clientGetSensor(sensorUrl, namelist, sys.argv[1], sys.argv[2])
