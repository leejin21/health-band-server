import requests
import json

import tokenEx

hearturl = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/sensorData/heartRate/"
tempHumidurl = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/sensorData/tempHumid/"
soundurl = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/sensorData/sound/"


def clientGetSensor(sensorUrl):
    headers = {"Authorization": tokenEx.token_h()}

    response = requests.get(
        soundurl, headers=headers)
    print(sensorUrl.split('/')[-2])
    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    sensorUrl = hearturl
    clientGetSensor(sensorUrl)


'''
    temp humid
avg  20   60
max  30   70
min  10   50

    heartRate
avg     90
max     100
min     80

    sound
avg  30
max  40
min  20


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


'''
