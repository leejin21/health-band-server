import requests
import json
import time
from datetime import datetime
import tokenEx

from pprint import pprint
# (TEMP, HUMID)
N1 = (27, 40, 'N1')
N2 = (28, 55, 'N2')
A1 = (29, 70, 'A1')
A2 = (31, 70, 'A2')
B1 = (32, 80, 'B1')
B2 = (33, 75, 'B2')
C1 = (35, 80, 'C1')
C2 = (36, 85, 'C2')


SEQUENCE_1 = [A1]*2 + [A2]*3 + [B1]*5 + [B2]*6 + [A1, A2]*2 + [A1]
SEQUENCE_2 = [B1, B2] + [A2]*13 + [A1]*6
SEQUENCE_3 = [A1, A2]*5 + [N2]*4 + [B1]*5 + [A1, A2]*5 + [B2]*6

# 마지막에 1개 더 추가해줘야 함.


def client(SEQUENCE):
    '''
    POST
    3초마다 post해주기: 20초짜리, 40초짜리, 80초짜리 이렇게.
    ==> 따라서 7번, 14번, 28번
    '''
    headers = {"Authorization": tokenEx.token_h("w3")}

    # wearerData/post

    for i in range(len(SEQUENCE)):
        data = dict()
        data['temp'], data['humid'], name = SEQUENCE[i]
        data['heartRate'] = "47"
        data['stepCount'] = "2000"

        response = requests.post(
            "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=data)
        # print(data)

        print(name)
        print("Status Code:", response.status_code)
        response_data = response.json()
        print(response_data)
        time.sleep(3)
        # 딱 3초 아니고 약 3.1초 정도 차이 남.


def calHeatIndex(temp, humid):
    temp = temp * 9/5 + 32
    heatIndex = -42.379 + 2.04901523 * temp + 10.14333127 * humid - 0.22475541 * temp * humid - 0.00683770 * temp * temp - 0.05481717 * humid * humid + 0.00122874 * temp * temp * humid + 0.00085282 * \
        temp * humid * humid - 0.00000199 * temp * temp * humid * humid
    return (heatIndex - 32) / 1.8


if __name__ == "__main__":
    # temp, humid, _ = C2
    # print(calHeatIndex(temp, humid))

    client(SEQUENCE_3)
