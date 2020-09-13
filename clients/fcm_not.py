import requests
import json

# 이대로 하기
"

def send_fcm_notification():
    # fcm 푸시 메세지 요청 주소
    url = "https://fcm.googleapis.com/fcm/send"
    # 인증 정보(서버 키)를 헤더에 담아 전달

    server_key = "my_sever_key",
    headers = {
        'Authorization': 'key= ' + server_key,
        'Content-Type': 'application/json; UTF-8',
    }

    # 보낼 내용과 대상을 지정
    # ids 존재 안하면 에러 발생하게 하기.
    content = {
        'to': "android_key",
        'data': {
            'title': "gkgk",
            'message': "w2님의 디바이스에서 낙상을 감지했습니다."
        }
    }

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    response = requests.post(
        url, data=json.dumps(content), headers=headers)
    print("status_code:", response.status_code)
    response_data = response.json()
    print(response_data)


send_fcm_notification()
