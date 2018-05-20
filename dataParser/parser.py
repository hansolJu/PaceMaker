import os,re,time
from bs4 import BeautifulSoup
from selenium import webdriver

from dataParser.models import *



class KutisParser(object):
    """Parse something from table of kutis website."""

    def __init__(self):
        self.base_url = "http://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp"
        self.login_url = "http://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp"
        self.studentInfoUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj111s.jsp?submenu=1&m_menu=wsco1s02&s_menu=wshj111s'
        self.studentHopeCareersUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj190s.jsp?m_menu=wsco1s02&s_menu=wshj190s'
        self.studentgradeUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssj1/wssj170s.jsp?submenu=2'
        self.page = str(1)
        self.year = str(2018)
        self.semester = str(10)
        self.scheduleUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp?curPage=" + self.page + "&hakgwa_cd=91017&gyear=" + self.year + "&gwamok_name=&ghakgi=" + self.semester
        self.subjectUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu5/wssu511s.jsp?year=2018&hakgi=10&jojik=A1000&gwamok_no=1199&gyosu_no=20100118&gwajung=1"
        #
        self.driverPath = abspath = os.path.abspath("static/parser/chromedriver.exe")
        self.driver = webdriver.Chrome(self.driverPath)
        self.driver.implicitly_wait(3)

    def login(self, id , pw):
        # url에 접근한다.
        self.driver.get(self.login_url)
        # 아이디/비밀번호를 입력해준다.
        self.driver.find_element_by_name("id").send_keys(id)
        self.driver.find_element_by_name('pw').send_keys(pw)
        # 로그인 버튼을 눌러주자.
        btn = self.driver.find_element_by_css_selector('#login_scroll > form > fieldset > p > a')
        btn.click()

        # 로그인이 됬는지 확인 하기.
        try:
            self.driver.get(self.studentInfoUrl)
        except:
            print("Kutis password 가 틀렸습니다.")
            time.sleep(1000)
            return False

    def get_original_data(self, url):
        """Get source from web and returns BeautifulSoup object."""
        self.driver.get(url)
        html = self.driver.page_source
        return BeautifulSoup(html, "html.parser")

    @staticmethod
    def get_table_data(Obj, table_list):
        """get table from original data and returns BeautifulSoup object."""
        return Obj.findAll("table", {'class': table_list})

    @staticmethod
    def parse_string_to_int(duration, default=0):
        """Try to parse string to int, or return default value."""
        try:
            return int(duration)
        except ValueError:
            return default

    @staticmethod
    def remove_html_tags(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def parse_item(self,item):
        pass


class StudentInfoParser(KutisParser):
    def parse_item(self,url):
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        i = 0
        infos = dict()
        resultTd = []
        resultTh = []
        tables = soup.findAll("table", {'class': 'list06'})

        for table in tables:
            # print(type(table))
            tds = table.findAll("td")
            ths = table.findAll("th")
            for th in ths:
                removeTag = KutisParser.remove_html_tags(str(th))
                resultTh.append(removeTag)
            for td in tds:
                removeTagTd = KutisParser.remove_html_tags(str(td))
                removeTagTd = removeTagTd.replace('\xa0', "")
                removeTagTd = removeTagTd.replace('\n', "")
                removeTagTd = removeTagTd.replace('\t', "")
                removeTagTd = removeTagTd.replace('변동내역', "")
                removeTagTd = removeTagTd.replace('※ 본인인증은 개인정보 변경에서 하시기 바랍니다.', "")
                print(removeTagTd)
                resultTd.append(removeTagTd)
        i = 0
        for th in resultTh:
            print("%d" % i, th)
            i += 1
        i = 0
        for td in resultTd:
            print("%d" % i, td)
            i += 1
        """Make Student information object with table Crawling data and dictionary."""
        # 학번
        infos['hukbun'] = resultTd[1]
        # 성명
        infos['name'] = resultTd[2]
        # 주민등록번호
        infos['jumin'] = resultTd[3]
        # 한자성명
        infos['name_Hanja'] = resultTd[4]
        # 영문성명
        infos['name_English'] = resultTd[5]
        # 과정구분
        # 캠퍼스구분
        infos['campus'] = resultTd[7]
        # 주야구분
        infos['dayNight'] = resultTd[8]
        # 학적구분
        infos['state'] = resultTd[9]
        # 학적변동
        infos['variance'] = resultTd[10]
        # 졸업학점
        infos['graduationCredit'] = resultTd[11]
        # 전공
        infos['major'] = resultTd[12]
        # 지도교수
        infos['advisor'] = resultTd[13]
        # 학생구분14
        # 산업체여부15
        # 학점교류구분116
        # 병역구분17
        # 현 학년학기
        infos['currentGrade'] = resultTd[18]
        # 이수학기 / 편입인정학기
        infos['compleSemester'] = resultTd[19]
        # 조기졸업대상여부
        infos['earlyGraduation'] = resultTd[20]
        # 특기자구분21
        # 입학구분22
        # 입학일자23
        infos['admission'] = resultTd[23]
        # 인증구분
        infos['enginCertification'] = resultTd[24]
        # 본인인증25
        # 본적지주소26
        # 거주지주소27
        infos['address'] = resultTd[27]
        # 전화번호
        infos['phone'] = resultTd[28]
        # 전자우편
        infos['email'] = resultTd[29]
        # 휴대폰30
        infos['cellPhone'] = resultTd[30]
        # 카카오톡ID31
        # 메신저QQ32
        # blank 33
        # 보호자34
        # 관계35
        # 근무지36
        # 보호자주소37
        # 보호자전화번호38
        infos['parentsPhone'] = resultTd[38]
        # 취미39
        # 특기40
        # 혈액형41
        return infos

    def save_info(self, hukbun, infos):
        """Save info from student infomation list to database."""
        info_object = StudentInfo(hukbun=infos['hukbun'],
                                    # 성명
                                  name=infos['name'],
                                    # 주민등록번호
                                  jumin=infos['jumin'] ,
                                    # 한자성명
                                  name_Hanja=infos['name_Hanja'],
                                    # 영문성명
                                  name_English=infos['name_English'] ,
                                    # 과정구분
                                    # 캠퍼스구분
                                  campus=infos['campus'] ,
                                    # 주야구분
                                  dayNight=infos['dayNight'] ,
                                    # 학적구분
                                  state=infos['state'],
                                    # 학적변동
                                  variance=infos['variance'] ,
                                    # 졸업학점
                                  graduationCredit=infos['graduationCredit'],
                                    # 전공
                                  major=infos['major'] ,
                                    # 지도교수
                                  advisor=infos['advisor'],
                                    # 현 학년학기
                                  currentGrade=infos['currentGrade'] ,
                                    # 이수학기 / 편입인정학기
                                  compleSemester=infos['compleSemester'] ,
                                    # 조기졸업대상여부
                                  earlyGraduation=infos['earlyGraduation'] ,
                                    # 입학일자23
                                  admission=infos['admission'],
                                    # 인증구분
                                  enginCertification=infos['enginCertification'],
                                    # 거주지주소27
                                  address=infos['address'],
                                    # 전화번호
                                  phone=infos['phone'],
                                    # 전자우편
                                  email=infos['email'] ,
                                    # 휴대폰30
                                  cellPhone=infos['cellPhone'] ,
                                    # 보호자전화번호38
                                  parentsPhone=infos['parentsPhone']
                                    )
        info_object.save()


class StudentGradePaser(KutisParser):

    def parse_item(self, url):
        # 리스트로 반환
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        i = 0
        infos = dict()

        resultTh = []
        resultTr = []
        tables = soup.findAll("table", {'class': 'list06'})

        for table in tables:
            # tr로 분리
            trs = table.findAll("tr")
            # th와 td로 분리
            for tr in trs:
                ths = tr.findAll("th")
                for th in ths:
                    removeTag = self.remove_html_tags(str(th))
                    resultTh.append(removeTag)

                tds = tr.findAll("td")
                resultTd = []
                for td in tds:
                    removeTagTd = self.remove_html_tags(str(td))
                    removeTagTd = removeTagTd.replace('\xa0', "")
                    removeTagTd = removeTagTd.replace('\n', "")
                    removeTagTd = removeTagTd.replace('\t', "")
                    removeTagTd = removeTagTd.replace('변동내역', "")
                    resultTd.append(removeTagTd)
                if resultTd:
                    if '이수구분별' in resultTd[0]:
                        findIndex = resultTr.__len__()
                        # print(findIndex,resultTr)
                        tmpindex = 0
                        tmp = ''
                        for i in range(findIndex, 0, -1):
                            if resultTr[i - 1].__len__() == 9:
                                tmpindex = i
                                tmp = resultTr[i - 1][0]
                                # print("복사할 정보",tmp,tmpindex)
                                break

                        for i in range(findIndex, tmpindex, -1):
                            if resultTr[i - 1].__len__() == 8:
                                resultTr[i - 1].insert(0, tmp)
                                # print(resultTr[i-1])
                    else:
                        resultTr.append(resultTd)
        # print(resultTh)
        # print(resultTr)
        return resultTr

    def save_info(self, hukbun, infos):
        # 리스트를 저장
        for td in infos:
            info_object = StudentGrade(hukbun_id = hukbun,
                                       # 이수구분
                                       eisu=td[0],
                                       # 인증구분
                                       certification=td[1],
                                       # 년도학기
                                       yearNsemester=td[2],
                                       # 학수코드
                                       subject_code=td[3],
                                       # 교과목명
                                       subject=td[4],
                                       # 학점
                                       # 설계학점
                                       grade_design=td[6],
                                       # 등급
                                       grade =td[7],
                                       # 유효구분
                                       valid =td[8],
                                       )
            info_object.save()