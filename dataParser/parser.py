import os,re,time
from bs4 import BeautifulSoup
from selenium import webdriver
from dataParser.models import *


class KutisParser(object):
    """Parse something from table of kutis website."""

    def __init__(self):
        self.base_url = "http://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp"
        self.login_url = "http://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp"

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

class StudentParser(KutisParser):
    studentInfoUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj111s.jsp?submenu=1&m_menu=wsco1s02&s_menu=wshj111s'
    studentHopeCareersUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj190s.jsp?m_menu=wsco1s02&s_menu=wshj190s'
    studentgradeUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssj1/wssj170s.jsp?submenu=2'
    def parse_info(self):
        """
        학생정보를 parse 후 dict object에 담아 리턴한다.
        :return: infos(dict Object)
        """
        soup = self.get_original_data(self.studentInfoUrl)

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
        '''for debug'''
        # i = 0
        # for th in resultTh:
        #     print("%d" % i, th)
        #     i += 1
        # i = 0
        # for td in resultTd:
        #     print("%d" % i, td)
        #     i += 1

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
        infos['course'] = resultTd[6]
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
        # 학생구분
        # 산업체여부
        # 학점교류구분
        # 병역구분
        # 현 학년학기
        infos['currentGrade'] = resultTd[18]
        # 이수학기 / 편입인정학기
        infos['compleSemester'] = resultTd[19]
        # 조기졸업대상여부
        infos['earlyGraduation'] = resultTd[20]
        # 특기자구분
        # 입학구분
        # 입학일자
        infos['admission'] = resultTd[23]
        # 인증구분
        infos['enginCertification'] = resultTd[24]
        # 본인인증
        # 본적지주소
        # 거주지주소
        infos['address'] = resultTd[27]
        # 전화번호
        infos['phone'] = resultTd[28]
        # 전자우편
        infos['email'] = resultTd[29]
        # 휴대폰
        infos['cellPhone'] = resultTd[30]
        # 카카오톡ID
        # 메신저QQ
        # blank
        # 보호자
        # 관계
        # 근무지
        # 보호자주소
        # 보호자전화번호
        infos['parentsPhone'] = resultTd[38]
        # 취미39
        # 특기40
        # 혈액형41
        return infos

    def save_info(self, hukbun, infos):
        """Save info from student infomation list to database."""
        info_object = StudentInfo(
            hukbun=infos['hukbun'],
            # 성명
            name=infos['name'],
            # 주민등록번호
            jumin=infos['jumin'] ,
            # # 한자성명
            # name_Hanja=infos['name_Hanja'],
            # # 영문성명
            # name_English=infos['name_English'] ,
            # 과정구분
            course=infos['course'],
            # # 캠퍼스구분
            # campus=infos['campus'] ,
            # # 주야구분
            # dayNight=infos['dayNight'] ,
            # 학적구분
            state=infos['state'],
            # 학적변동
            variance=infos['variance'] ,
            # 졸업학점
            gradeCredit=infos['graduationCredit'],
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
            # # 거주지주소27
            # address=infos['address'],
            # # 전화번호
            # phone=infos['phone'],
            # # 전자우편
            # email=infos['email'] ,
            # # 휴대폰30
            # cellPhone=infos['cellPhone'] ,
            # # 보호자전화번호38
            # parentsPhone=infos['parentsPhone']
        )
        info_object.save()

    def parse_grade(self):
        """
        parse grade data, and return tds_list Object.
        :return: resultTr--> listObject
        """
        soup = self.get_original_data(self.studentgradeUrl)

        resultTr = []
        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:
            # tr로 분리
            trs = table.findAll("tr")
            # th와 td로 분리
            for tr in trs:

                ths = tr.findAll("th")
                resultTh = [] # for문안에서 사용후 제거.
                for th in ths:
                    removeTag = self.remove_html_tags(str(th))
                    resultTh.append(removeTag)

                tds = tr.findAll("td")
                resultTd = [] # for문안에서 사용후 제거.
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

    def save_grade(self,hukbun, tdLists):
        """ td단위로 구성된 리스트를 DB에 저장한다. """
        for td in tdLists:
            info_object = StudentGrade(
                hukbun_id=hukbun,
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
                grade=td[7],
                # 유효구분
                valid=td[8]
            )
            info_object.save()

    def parse_hope(self):
        """
        parse Hope data, and return tds_list Object.
        :return: resultTr--> listObject
        """
        soup = self.get_original_data(self.studentHopeCareersUrl)

        resultTr = []
        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:
            ths = table.findAll("th")
            resultTh = [] # for문안에서 사용후 제거.
            for th in ths:
                removeTag = KutisParser.remove_html_tags(str(th))
                resultTh.append(removeTag)

            tds = table.findAll("td")
            resultTd = [] # for문안에서 사용후 제거.
            for td in tds:
                removeTagTd = KutisParser.remove_html_tags(str(td))
                removeTagTd = removeTagTd.replace('\xa0', "")
                removeTagTd = removeTagTd.replace('\n', "")
                removeTagTd = removeTagTd.replace('\t', "")
                removeTagTd = removeTagTd.replace('변동내역', "")
                print(removeTagTd)
                resultTd.append(removeTagTd)
            #resultTd에 아무정보 없으면 저장X(Th 단 걸러내기)
            if resultTd:
                pass
            else:
                resultTr.append(resultTd)
        return resultTr

        '''for debuging'''
        #i = 0
        # for th in resultTh:
        #     print("%d" % i, th)
        #     i += 1
        # i = 0
        # for td in resultTd:
        #     print("%d" % i, td)
        #     i += 1

    def save_hope(self,hukbun,tdLists):
        """ td단위로 구성된 리스트를 DB에 저장한다. """

        for td in tdLists:
            info_object = StudentHopeCareers(
                hukbun_id=hukbun,
                # 진로구분
                careers=td[0],
                # 지망순위
                ranking=td[1],
                # 지망순위
                # 직업(소분류)
                job=td[3],
                # 희망기업
                Enterprise=td[4],
                # 희망연봉
                Salary=td[5],
                # 희망근무지역
                Address=td[6]
            )
            info_object.save()


class ServerParser(KutisParser):
    """Crawing Semester Schedule and parse data """

    def parse_course_major(self, year, semester):
        """년도와 원하는 학기를 받으면 해당 년도 학기에 열린 과목의 정보를 크롤하여 parse한후 리스트에 담아서 리턴한다.
        :param: year(찾고자하는 년도){2009~2018}
        :param: semester(찾고자 하는 학기) {1,2}
        :return:(list)
        """
        # 파라미터 초기화
        year = (str)(year)

        if semester == 1:
            semester = (str)(10)
        elif semester == 2:
            semester = (str)(20)
        else:
            print("학기 오류 1학기로 초기화")
            semester = (str)(10)

        # find total page num
        page = 1
        scheduleUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp?curPage=" \
                      + (str)(page) + "&hakgwa_cd=91017&gyear=" + year + "&gwamok_name=&ghakgi=" + semester
        soup = self.get_original_data(scheduleUrl)

        pages = (str)(soup.findAll("p", {'class': 'fr'}))
        totalpage = int(re.findall('\d+', pages)[0])

        resultTh = []
        resultTr = []
        while (True):
            tables = soup.findAll("table", {'class': 'list02'})
            for table in tables:
                trs = table.findAll("tr")

                for tr in trs:
                    # 같은내용 두번수행 방지
                    if resultTh:
                        pass
                    else:
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
                        removeTagTd = removeTagTd.replace('       보기', "")
                        removeTagTd = removeTagTd.replace('보기', "")
                        resultTd.append(removeTagTd)
                    # resultTd에 아무정보 없으면 저장X(Th 단 걸러내기)
                    if resultTd:
                        resultTr.append(resultTd)
                    else:
                        pass
            # print(page) # for debuging
            # 다른 페이지도 크롤링
            if page >= totalpage:
                break
            else:
                page += 1
                scheduleUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp?curPage=" \
                              + (str)(page) + "&hakgwa_cd=91017&gyear=" + year + "&gwamok_name=&ghakgi=" + semester
                soup = self.get_original_data(scheduleUrl)

        '''for debuging'''
        # # 결과물 출력
        # print(resultTh)
        # for td in resultTr:
        #     print(td)
        return resultTr


    def save_course_major(self, year, semester, tdLists):
        """ td단위로 구성된 리스트를 DB에 저장한다. """
        for td in tdLists:
            info_object = StudentHopeCareers(
                # 년도
                year = year,
                # 학기
                semester = semester,
                # 과목번호
                subjectCode=td[0],
                # 과목이름
                subjectName=td[1],
                # 추천학년(학교에서)
                grade=td[2],
                # 이수구분
                eisu=td[3],
                # 학점
                score=td[4],
                # 담당교수
                professor=td[5],
                # 비고
                remarks=td[6],
                # 교시
                time=td[7],
                # 강의실
                lectureRoom=td[8]
            )
            info_object.save()

    # course_num = 그학기에 해당하는 과목번호
    def parse_course_detail(self,year, semester, course_num, profess_num):
        url = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu5/wssu511s.jsp?" \
              "year="+str(year)+ \
              "&hakgi="+str(semester)+ \
              "&jojik=A1000" \
              "&gwamok_no="+str(course_num)+ \
              "&gyosu_no="+str(profess_num)+ \
              "&gwajung=1"
        soup = self.get_original_data(url)
        result = []
        tables = soup.findAll("table", {'class': 'list06'})
        # table[1] 교과목 해설
        Course_description_th = self.remove_html_tags(str(tables[1].findAll("th")))
        Course_description = self.remove_html_tags(str(tables[1].findAll("td")[0]))
        result.append(Course_description)
        print(Course_description_th)
        print(Course_description)
        print("----------------")
        # table[2] 새부핵심역량 과의 관계
        Core_Competencies_th = self.remove_html_tags(str(tables[2].findAll("th")))
        Core_Competencies = tables[2].findAll("td")
        list = []
        for td in Core_Competencies:
            list.append(self.remove_html_tags(str(td)))
        result.append(list)
        print(Core_Competencies_th)
        print(Core_Competencies)
        print("----------------")

        # table[3] 교과목 학습목표 및 평가방법 td 갯수세기
        evaluation_th = self.remove_html_tags(str(tables[3].findAll("th")))
        rows = tables[3].findAll("tr")

        count = 0
        tmp = ''
        nextRow = False
        resultRow = []

        for columns in rows:
            resultColumn = []
            columns = columns.findAll("td")
            if nextRow == True:
                resultColumn.append(tmp)
                count -= 1
            for column in columns:
                # 핵심역량인지 판별한후, 맞으면 저장, 몇번해야할지도 저장
                if 'rowspan' in str(column):
                    tmp = self.remove_html_tags(str(column))
                    count = int(re.findall('\d+', str(column))[0]) - 1
                resultColumn.append(self.remove_html_tags(str(column)).replace('\n', ""))
                # print("result column :",resultColumn)

            if resultColumn:
                resultRow.append(resultColumn)

            # 핵심역량을 몇번 출력할지 확인
            if count != 0:
                nextRow = True
            else:
                nextRow = False
                tmp = ''

        result.append(resultRow)
        print(evaluation_th)
        print(resultRow)
        print("----------------")

        # table[4] 강의방법 <input 으로 split 후 'checked'을 포함하는지 확인후, 테그삭제후 리턴
        Lecture_method_th = self.remove_html_tags(str(tables[4].findAll("th")))
        print(Lecture_method_th)
        Lecture_methods = tables[4].findAll("td")
        result_td = []
        for Lecture_method in Lecture_methods:
            tdRemove = (str)(Lecture_method)
            tdRemove = tdRemove.replace('\xa0', "")
            tdRemove = tdRemove.replace('\n', "")
            tdRemove = tdRemove.replace('\t', "")
            # print(tdRemove)
            tdRemove = tdRemove.split('<input')

            # print(tdRemove)
            for i in tdRemove:
                # print(i)
                if 'checked' in i:
                    i = '<input' + i
                    i = self.remove_html_tags(i)
                    result_td.append(i)
        result.append(result_td)
        print(result_td)
        print("------------------")

        # table[5] 과제물
        Assignment_th = self.remove_html_tags(str(tables[5].findAll("th")))
        Assignment = self.remove_html_tags(str(tables[5].findAll("td")[0]))

        result.append(Assignment)
        print(Assignment_th)
        print(Assignment)
        print("----------------")

        # table[6] 성적 구성비율 존나 머리 안돌아가서 하드코딩되있음.
        composition_ratio = self.remove_html_tags(
            str(tables[6].findAll("td")).replace('\n', "").replace("\t", "").replace("\xa0", ""))
        list = composition_ratio.replace('[', "").replace(']', "").split(",")

        th = []
        td = []
        for i in list:
            th_td = i.split(" ")
            if th_td.__len__() > 2:
                th.append(th_td[0] + th_td[1] + th_td[2])
                td.append(th_td[3])

                th.append(th_td[5])
                td.append(th_td[7])
            else:
                th.append(th_td[0])
                td.append(th_td[1])
        result.append(td)
        print(th)
        print(td)
        print("----------------")

        # table[7] 주별 강좌내용
        course_contents_th = self.remove_html_tags((str)(tables[7].findAll("th")))
        rows = tables[7].findAll("tr")
        resultRow_course = []
        for columns in rows:
            resultColumn = []
            columns = columns.findAll("td")
            for column in columns:
                resultColumn.append(
                    self.remove_html_tags(str(column)).replace('\n', "").replace("\t", "").replace("\xa0", ""))
                # print("result column :",resultColumn)
            if resultColumn:
                resultRow_course.append(resultColumn)

        result.append(resultRow_course)
        print(course_contents_th)
        print(resultRow_course)

        print("----------------")

        # table[8] 책
        book_th = self.remove_html_tags((str)(tables[8].findAll("th")))
        book = tables[8].findAll("td")
        list = []
        for td in book:
            list.append(self.remove_html_tags(str(td)))
        result.append(list)
        print(book_th)
        print(book)
        print("----------------")
        return result


    def save_course_detail(self,year, semester, course_num, list):
        info_object = Subject_desription(
            year = year,
            semester = semester,
            subjectCode= course_num,
            desription = list[0]
        )
        info_object.save()

        info_object = Core_Competence(
            year=year,
            semester=semester,
            subjectCode=course_num,
            # [지식응용, 검증능력, 문제해결, 도구활용, 설계능력, 팀웍스킬, 의사전달, 영향이해, 책임의식, 자기주도]
            Knowledge_application=list[1][0],
            verification_ability = list[1][1],
            problem_solving = list[1][2],
            tool_utilization = list[1][3],
            design_ability = list[1][4],
            teamwork_skill = list[1][5],
            communication = list[1][6],
            understanding_of_influence = list[1][7],
            responsibility = list[1][8]

        )
        info_object.save()
        for i in list[2]:
            info_object = Learning_Objectives(
                year=year,
                semester=semester,
                subjectCode=course_num,
                Core_competencies=i[0],
                detailed_core_competencies = i[1],
                reflectance = i[2],
                learning_objectives = i[3],
                performance_criteria = i[4],
                achievement_goals = i[5],
                evaluation_methods = i[6],
            )
            info_object.save()

        info_object = Lecture_method(
            year=year,
            semester=semester,
            subjectCode=course_num,
            # [강의형태, 수업방식, 교육용기자재]
            Lecture_type=list[3][0],
            teaching_method = list[3][1],
            educational_equipment = list[3][2]
        )
        info_object.save()

        info_object = Assignment(
            year=year,
            semester=semester,
            subjectCode=course_num,
            Assignment=list[4]
        )
        info_object.save()

        info_object = School_composition_ratio(
            year=year,
            semester=semester,
            subjectCode=course_num,
            Midterm_exam=list[5][0],
            final_exam = list[5][1],
            attendance = list[5][2],
            assignments_and_others = list[5][3],
            grading_division = list[5][4]
        )
        info_object.save()
        for i in list[6]:
            info_object = Weekly_course_contents(
                year=year,
                semester=semester,
                subjectCode=course_num,

                week=i[0],
                contents = i[1],
                methods = i[2],
                related_materials = i[3],
                assignments = i[4]
            )
            info_object.save()

        info_object = Book(
            year=year,
            semester=semester,
            subjectCode=course_num,
            title=list[7][0],
            author = list[7][1],
            publisher = list[7][2],
            year_of_publication = list[7][3],
        )
        info_object.save()
