import re
import rsa
import json
import requests
from bs4 import BeautifulSoup
from .response import AuthResponse

class SCHUAuth:
    def __init__(self):
        self._session = requests.Session()

    def authenticate(self, user_id: str, password: str) -> AuthResponse:
        if not self._login(user_id, password):
            raise ValueError("로그인에 실패했습니다. 인증 정보를 확인해주세요.")
        
        user_info = self._get_user_info()
        if user_info:
            user_info.user_id = user_id
        return user_info

    def _get_user_info(self) -> AuthResponse:
        url = 'https://id.sch.ac.kr/Career/LeftMenuView.aspx'
        response = self._session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        name_section = soup.find('h4', class_='col-lg-12 p-0 f500')
        info_sections = soup.find_all('h6', class_='col-lg-12 p-0')

        if not name_section or len(info_sections) < 2:
            raise ValueError("사용자 정보를 가져오는 중 오류가 발생했습니다.")

        name, gender = self._parse_name_and_gender(name_section.text.strip())
        major_grade = info_sections[0].text.strip()
        major, grade = major_grade.split(' ')
        grade = grade.replace('학년', '')
        professor = info_sections[1].text.strip().replace('지도교수 ', '')

        return AuthResponse(user_id=0, name=name, gender=gender, major=major, grade=grade, professor=professor)

    def _login(self, user_id: str, password: str) -> bool:
        url = 'https://id.sch.ac.kr/SSO/SSORequest.aspx?&rurl=&retU='
        response = self._session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find_all('script')[-1]

        sso_challenge, public_key = self._extract_sso_and_public_key(script)
        if not sso_challenge or not public_key:
            return False

        encrypted_credentials = self._rsa_encrypt(public_key, user_id, password, sso_challenge)

        login_data = {
            'login_endpoint': 'oauth',
            'retUrl': 'https://www.sch.ac.kr',
            'pw': encrypted_credentials,
            'id_type': 'H',
            'id': user_id,
            'passw': ""
        }

        login_response = self._session.post('https://sso.sch.ac.kr/oa/au/auth/verify', data=login_data)
        redirect_url = self._extract_redirect_url(login_response.text)

        if redirect_url:
            self._session.get(f"https://id.sch.ac.kr/{redirect_url}")
            return True

        return False

    @staticmethod
    def _extract_sso_and_public_key(script) -> tuple:
        if not script or not script.string:
            return None, None

        sso_match = re.search(r"'ssoChallenge'\s*:\s*'([^']*)'", script.string)
        public_key_match = re.search(r'rsa\.setPublic\("([^"]+)",\s*"(\d+)"\);', script.string)

        sso_challenge = sso_match.group(1) if sso_match else None
        public_key = public_key_match.group(1) if public_key_match else None

        return sso_challenge, public_key

    @staticmethod
    def _rsa_encrypt(public_key: str, user_id: str, password: str, sso_challenge: str) -> str:
        n = int(public_key, 16)
        json_obj = {
            'userid': f"H{user_id}",
            'userpw': password,
            'ssoChallenge': sso_challenge
        }
        json_str = json.dumps(json_obj)

        pubkey = rsa.PublicKey(n, 65537)
        encrypted = rsa.encrypt(json_str.encode(), pubkey)

        return encrypted.hex()

    @staticmethod
    def _extract_redirect_url(text: str) -> str:
        match = re.search(r"top\.location\.href='([^']+)';", text)
        return match.group(1) if match else None

    @staticmethod
    def _parse_name_and_gender(name: str) -> tuple:
        try:
            name, gender = name.split('(')
            return name.strip(), gender.replace(')', '').strip()
        except ValueError:
            return name.strip(), ""
