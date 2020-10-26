import requests
import json
import time
import sys
import random

import tokenEx
import ex_dicts


def post_other(user, data):
    headers = {"Authorization": tokenEx.token_h(user)}

    # wearerData/post
    if type(data) == list:
        for d in data:
            print(d)
            response = requests.post(
                "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=d)
            print("Status Code:", response.status_code)
            response_data = response.json()
            print(response_data)
            time.sleep(1)

    else:
        response = requests.post(
            "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/", headers=headers, data=data)

        print("Status Code:", response.status_code)
        response_data = response.json()
        print(response_data)


def post_meter(user, data):
    headers = {"Authorization": tokenEx.token_h(user)}

    # wearerMeter/post/

    response = requests.post(
        "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerMeter/post/", headers=headers, data=data)

    print("Status Code:", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    # 정상
    # post_other(sys.argv[1], ex_dicts.normal_example(10))
    # post_meter(sys.argv[1], {'meter': str(90)})

    # 14. 빈맥성 부정맥 test
    post_other(sys.argv[1], ex_dicts.heart_example("b", 20))

    # 15. 열사병 위험 test
    # post_other(sys.argv[1], ex_dicts.sum_event("C", 15))
