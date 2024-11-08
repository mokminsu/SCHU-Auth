# 순천향대학교 재학생 인증 라이브러리 입니다.

개발 기간 : 2024.11.01 ~ 2023.11.08

## 프로젝트 소개
파이썬으로 순천향대학교 크롤링을 이용해 학번 + 비밀번호를 통한 재학생 정보를 알아오는 라이브러리입니다.

## 개발환경
* 운영체제 : Windows 11 x64 (24H2, 26100.2033)
* 사용 언어 : Python 3.13.0
* 요구 라이브러리 : [BeautifulSoup4(4.12.3)](https://pypi.org/project/beautifulsoup4/), [requests(2.32.3)](https://pypi.org/project/requests/), [rsa(4.9)](https://pypi.org/project/rsa/)

## 설치하기

### 라이브러리 설치
```bash
pip install SCHU_Auth
```

## 실행하기

### 바로 실행하기
```py3
from schu_auth.auth import SCHUAuth

auth = SCHUAuth()

user_id = 'your_user_id'
password = 'your_password'

user_info = auth.authenticate(user_id, password)

print("이름:", user_info.name)
print("성별:", user_info.gender)
print("전공:", user_info.major)
print("학년:", user_info.grade)
print("지도교수:", user_info.professor)
```

## 함수 설명
* **authenticate** : 로그인 수행 후 재학생 정보를 수집하는 함수

## 반환 타입
```py3
class AuthResponse:
    user_id: str
    name: str
    gender: str
    major: str
    grade: str
    professor: str
```

## 예외 설명
* **ValueError** : 인증 정보 오류 또는 사이트 장애시 발생하는 예외

## 사용 스택

### 개발 환경
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)             

### 개발 언어
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffffff)

## 유의사항
이 프로젝트는 일반 사용자가 로그인하는 흐름을 프로그래밍 적으로 따라하여 로그인을 진행합니다.

해당 프로젝트는 재학생의 정보 무결성을 보장하지 않으며, 사용시 발생하는 모든 법적 문제를 책임지지 않습니다.

프로젝트상의 문제, 비공개 요청시 <a href="mailto:contact@mokminsu.dev" target="_blank">contact@mokminsu.dev</a> 로 연락바랍니다


## 라이센스
이 프로젝트는 [MIT License](LICENSE)로 배포됩니다.
