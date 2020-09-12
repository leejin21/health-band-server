# health-band: server

처음 시작할 때 ~/main 에서 `workon djangoEnv`로 가상환경 접속하기

서버 시작할 때, 이 글
(https://velog.io/@tera_geniel/nohup-%EB%AA%85%EB%A0%B9%EC%96%B4-putty%EC%97%90%EC%84%9C-%EC%93%B0%EA%B8%B0)
 참고하면서 runserver 명령어 돌리기
```bash
(djangoEnv) ~/main$ python manage.py runserver

```


## environment

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

## 회원가입, 로그인 기능

https://velog.io/@tera_geniel/django-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EA%B4%80%EB%A0%A8
에 대부분의 에러 사항과 어떻게 고친 건 지를 적어둠.

아직 회원타입 관련 custom은 못한 상태

### end points
```wearerData/post/ (POST)

```



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

## Custom User model

validate_^field^에서 return value에 value 대신 다른 값을 넣으면 해당 값으로 save된다는 데서 착안하여 
foreign field를 2개 넣은 model serializer function 만드는 데 성공함.(src/users/serializers.py 참고, validate_함수 이용)



## authentication_classes 관련 이슈



## clients/hana.py 관련 설명

## wearer data 저장 관련 이슈
- clients/hana.py
login용, wearerData 저장용, linkedUser 저장용 등을 만들어야 함(아직 예쁘게 정리되지 않은 상태)
- Wearer Data의 time에 timezone 관련하여 KR 시간으로 저장이 안된다. KR 시간으로 저장되도록 해야 함.