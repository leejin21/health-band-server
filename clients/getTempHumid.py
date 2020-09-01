import requests
import json

import tokenEx


def clientTempHumid():
    headers = {"Authorization": tokenEx.token_h()}

    response = requests.get(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/sensorData/tempHumid/", headers=headers)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    clientTempHumid()
