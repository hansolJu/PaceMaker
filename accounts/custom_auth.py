import requests
from bs4 import BeautifulSoup as bs
def check_if_user(user_id, user_pw):
    with requests.Session() as s:
        id = user_id
        password = user_pw
        page = "http://kutis.kyonggi.ac.kr:2012/servlets/core/login?attribute=login&token1=kguv_sugang1&token=kguv_sugang" \
               "&id=" + id + \
               "&password=" + password
        first_page = s.get(page)
        html = first_page.text
        soup = bs(html,'html.parser')
        script = soup.findAll("script")
        a= str(script).split(">")[1].split('"')[1]
        # print(a)

        if '재학생이 아닙니다.' in a:
            print("학교 학생이 아님")
            return False
        elif '학번/비밀번호가' in a:
            print("학번 또는 비밀번호 다름.")
            return False
        elif 'menuframe' in a:
            print("success")
            return True
        else:
            pass


#20001146 == 운영자 학번으로 추청
