# health-band: server

## explanation

2020 한이음 프로젝트 '헬스 솔로잉 밴드'의 서버를 구현한 레포지터리입니다.
자세한 설명 및 구동 모습은 아래 유투브 링크를 참고해 주세요.
https://www.youtube.com/watch?v=oZmZxbMW9MI

## environment

처음 시작할 때 ~/main 에서 `workon djangoEnv`로 가상환경 접속하기

서버 시작할 때, 이 글
(https://velog.io/@tera_geniel/nohup-%EB%AA%85%EB%A0%B9%EC%96%B4-putty%EC%97%90%EC%84%9C-%EC%93%B0%EA%B8%B0)
 참고하면서 runserver 명령어 돌리기
```bash
(djangoEnv) ~/main$ python manage.py runserver

```

| python | django | djangorestframework | pygments | mysql | mysqlclient | mysql-client-core | django-rest-auth | django-allauth | 
| :----: | :----: | :------------------:| :------: | :---: | :---------: | :---------------: | :--------------: | :----: |
| 3.6.9 | 3.0.3 | 3.11.0 | 2.5.2 | 5.7.30 | 2.0.1 | 5.7 | 0.9.5 | 0.42.0 |

```bash
sudo apt install python3-pip
sudo pip3 install virtualenvwrapper
mkvirtualenv djangoEnv
workon djangoEnv
```
을 통해 djangoEnv 아래에 위와 같이 django, djangorestframework, pygments 등의 환경을 구성하였다.
(https://learndjango.com/tutorials/official-django-rest-framework-tutorial-beginners 참고)

또한, vscode로 작업하면서

Successfully installed astroid-2.4.2 isort-4.3.21 lazy-object-proxy-1.4.3 mccabe-0.6.1 pylint-2.5.3 six-1.15.0 toml-0.10.1 typed-ast-1.4.1 wrapt-1.12.1

도 해주었고, python interpreter는 djangoEnv로 설정하였다.

++  
django-allauth를 다운받으며
Successfully installed certifi-2020.6.20 chardet-3.0.4 defusedxml-0.6.0 django-allauth-0.42.0 idna-2.10 oauthlib-3.1.0 python3-openid-3.2.0 requests-2.24.0 requests-oauthlib-1.3.0 urllib3-1.25.9

도 해주었다.

++ 
fcm-django-0.3.4 pyfcm-1.4.7

## database settings

```sql
create database health_db3 character set utf8mb4 collate utf8mb4_general_ci;
-- Query OK, 1 row affected (0.00 sec)
use health_db3
-- Database changed
show tables;
-- Empty set (0.01 sec)
```

## 예제 user 관련 설명

w1(착용일) ~ p1, p2, p3
w2(착용이) ~ p1, p2
"w3(착용삼) ~ p1, p3" => 영상에서 이걸로?

p1(보호일) ~ w1, w2, w3
p2(보호이) ~ w1, w2
p3(보호삼) ~ w1, w3

### end points

```/linkedUser/post (POST)
- wearer
- protector
- Returns newlinkeduser's information(username, name, user_type, phone_number)
- In the header, need to include the token: rf) clients/hana.py
```

```
/custom/login/ (POST)

- username
- email
- password
- Returns Token key, user data(username, name, user_type, phone_number)
```
```
/rest-auth/logout/ (POST)
```
```
/rest-auth/password/reset/ (POST)

- email
```
```
/rest-auth/password/reset/confirm/ (POST)

- uid
- token
- new_password1
- new_password2
```
```
/rest-auth/password/change/ (POST)

new_password1
new_password2
old_password
```

```
/rest-auth/user/ (GET, PUT, PATCH)

- username
- first_name
- last_name
Returns pk, username, email, first_name, last_name
```
```
Registration
/rest-auth/registration/ (POST)

- username
- password1
- password2
- email
```

#### end point - custom 0928

1. 보호자: 착용자 데이터 GET 요청
url = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/get/"
header: token
params: wearerId


{'data': {'heartRate': '47',
          'humid': '53',
          'meter': '3000',
          'nowDate': '2020-09-28',
          'nowTime': '23:17:01.343686',
          
          'temp': '17'},
 'status': 'success'}


2. 착용자: 미터수 POST 요청
url =  "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerMeter/post/"
header: token

data = {
    "meter": "500"
}


3. 착용자: 센서 데이터 POST 요청

url = "http://ec2-3-34-84-225.ap-northeast-2.compute.amazonaws.com:8000/wearerData/post/"
header: token

data = {
    "temp": "17",
    "humid": "53",
    "heartRate": "47",
    
}
