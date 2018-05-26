import re

import requests
from bs4 import BeautifulSoup

from dataParser.models import *


class KutisParser(object):
    """Parse something from table of kutis website."""

    def __init__(self, user_id, user_pw):
        print("객체 생성,", user_id, user_pw)
        self.s = self.login(user_id, user_pw)

    # 로그인후 섹션 반환
    @staticmethod
    def login(user_id, user_pw):
        LOGIN_URL = 'https://kutis.kyonggi.ac.kr/webkutis/view/hs/wslogin/loginCheck.jsp?'
        LOGIN_DATA = {'id': user_id, 'pw': user_pw}
        with requests.Session() as s:
            res = s.post(LOGIN_URL, data=LOGIN_DATA, verify=False, allow_redirects=False)
            return s

    @staticmethod
    def get_original_data(url, s):
        "Get source from web and returns BeautifulSoup object."
        html = s.get(url).text
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
    # print("StudentParser 객체 생성")
    def parse_info(self):
        """
        학생정보를 parse 후 dict object에 담아 리턴한다.
        :return: infos(dict Object)
        """
        print("학생정보 파싱 시작")
        studentInfoUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj111s.jsp?submenu=1&m_menu=wsco1s02&s_menu=wshj111s'
        soup = self.get_original_data(studentInfoUrl, self.s)

        i = 0
        resultTd = []
        resultTh = []
        result = []
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
            result.append(resultTd)
        '''for debug'''
        # i = 0
        # for th in resultTh:
        #     print("%d" % i, th)
        #     i += 1
        # i = 0
        # for td in resultTd:
        #     print("%d" % i, td)
        #     i += 1
        print("result: ", result)
        return result

    @staticmethod
    def save_info(tdLists):
        '''학생정보를 데이터베이스에 저장
        :param:tdList : parse_info()의 리턴값. 2차원 배열로 구성되어있음.
        '''
        for td in tdLists:
            oneLineinfo = StudentInfo(
                hukbun=td[1],
                # 성명 2
                username=td[2],
                # 주민등록번호 3
                jumin=td[3],
                # 한자성명 4
                # name_Hanja=infos[4],
                # 영문성명 5
                # name_English=infos[5] ,
                # 과정구분
                course=td[6],
                # 캠퍼스구분
                # campus=infos[7] ,
                # 주야구분
                # dayNight=infos[8] ,
                # 학적구분 9
                state=td[9],
                # 학적변동 10
                variance=td[10],
                # 졸업학점
                graduationCredit=td[11],
                # 전공
                major=td[12],
                # 지도교수
                advisor=td[13],
                # 학생구분 14
                # 산업체여부 15
                # 학점교류구분 16
                # 병역구분 17
                # 현 학년학기 18
                currentGrade=td[18],
                # 이수학기 / 편입인정학기
                compleSemester=td[19],
                # 조기졸업대상여부 20
                earlyGraduation=td[20],
                # 특기자구분 21
                # 입학구분22
                # 입학일자23
                admission=td[23],
                # 인증구분 24
                enginCertification=td[24],
                # 본인인증 25
                # 본적지주소 26
                # 거주지주소 27
                # address=td['address'],
                # # 전화번호
                # phone=td['phone'],
                # # 전자우편
                # email=td['email'] ,
                # # 휴대폰30
                # cellPhone=td['cellPhone'] ,
                # # 보호자전화번호38
                # parentsPhone=td['parentsPhone']
                # 카카오톡ID
                # 메신저QQ
                # blank
                # 보호자
                # 관계
                # 근무지
                # 보호자주소
                # 보호자전화번호
                # 취미39
                # 특기40
                # 혈액형41
            )
            oneLineinfo.save()

    def parse_grade(self):
        """
        parse grade data, and return tds_list Object.
        :return: resultTr--> listObject
        """
        studentgradeUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssj1/wssj170s.jsp?submenu=2'
        soup = self.get_original_data(studentgradeUrl, self.s)

        resultTr = []
        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:
            # tr로 분리
            trs = table.findAll("tr")
            # th와 td로 분리
            for tr in trs:

                ths = tr.findAll("th")
                resultTh = []  # for문안에서 사용후 제거.
                for th in ths:
                    removeTag = self.remove_html_tags(str(th))
                    resultTh.append(removeTag)

                tds = tr.findAll("td")
                resultTd = []  # for문안에서 사용후 제거.
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
                    elif resultTd.__len__() < 3:
                        pass
                    else:
                        resultTr.append(resultTd)
        # print(resultTh)
        print(resultTr)
        return resultTr

    @staticmethod
    def save_grade(hukbun, tdLists):
        """ 저장이나 업데이트를 위한 오브젝트 리스트를 만들어 객체리스트 리턴
        :param  hukbun: 저장할 학생의 학번 타입은 str ex)"20100000"
        :param tdLists: parse_grade()의 리턴값 , 이차원 배열
        """
        # 저장하기전에 학번의 성적을 다 지운다.
        StudentGrade.objects.filter(hukbun_id=hukbun).delete()
        for td in tdLists:
            oneLineinfo = StudentGrade(
                hukbun_id="201511868",
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
                score=td[5],
                # 설계학점
                grade_design=td[6],
                # 등급
                grade=td[7],
                # 유효구분
                valid=td[8]
            )
            oneLineinfo.save()

    def parse_hope(self):
        """
        parse Hope data, and return tds_list Object.
        :return: resultTr--> listObject
        """
        studentHopeCareersUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj190s.jsp?m_menu=wsco1s02&s_menu=wshj190s'
        soup = self.get_original_data(studentHopeCareersUrl, self.s)

        resultTr = []
        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:
            ths = table.findAll("th")
            resultTh = []  # for문안에서 사용후 제거.
            for th in ths:
                removeTag = KutisParser.remove_html_tags(str(th))
                resultTh.append(removeTag)

            tds = table.findAll("td")
            resultTd = []  # for문안에서 사용후 제거.
            for td in tds:
                removeTagTd = KutisParser.remove_html_tags(str(td))
                removeTagTd = removeTagTd.replace('\xa0', "")
                removeTagTd = removeTagTd.replace('\n', "")
                removeTagTd = removeTagTd.replace('\t', "")
                removeTagTd = removeTagTd.replace('변동내역', "")
                print(removeTagTd)
                resultTd.append(removeTagTd)
            # resultTd에 아무정보 없으면 저장X(Th 단 걸러내기)
            if resultTd:
                pass
            else:
                resultTr.append(resultTd)
        return resultTr

        '''for debuging'''
        # i = 0
        # for th in resultTh:
        #     print("%d" % i, th)
        #     i += 1
        # i = 0
        # for td in resultTd:
        #     print("%d" % i, td)
        #     i += 1

    @staticmethod
    def save_hope(hukbun, tdLists):
        """ td단위로 구성된 리스트를 DB에 저장한다. """
        StudentHopeCareers.objects.filter(hukbun_id=hukbun).delete()
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
    """Crawing 학기 수강가능과목 and parse data """

    def parse_course_major(self, year, semester):
        """년도와 원하는 학기를 받으면 해당 년도 학기에 열린 과목의 정보를 크롤하여 parse한후 리스트에 담아서 리턴한다.
        :param: year(찾고자하는 년도){2009~2018}
        :param: semester(찾고자 하는 학기) {1,2}
        :return:(list)
        """
        # 파라미터 초기화
        year = str(year)
        if semester == 1:
            semester = str(10)
        elif semester == 2:
            semester = str(20)
        else:
            print("학기 오류 1학기로 초기화")
            semester = str(10)

        # find total page num
        page = 1
        scheduleUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp?" \
                      "curPage=" + str(page) + \
                      "&hakgwa_cd=91017&gyear=" + year + \
                      "&gwamok_name=&ghakgi=" + semester
        soup = self.get_original_data(scheduleUrl)

        # 최대페이지 추적
        pages = str(soup.findAll("p", {'class': 'fr'}))
        totalpage = int(re.findall('\d+', pages)[0])

        # 교수 학번 디비 저장
        tds = soup.findAll("td")
        for td in tds:
            if "detailView_gyosu" in str(td):
                removeTag = self.remove_html_tags(str(td))
                name = removeTag.split("\r")[0]

                spans = td.findAll("span")[1]
                id = str(spans).split("\'")[3]

                # 하드코딩 디비저장
                if id in Professor.pk:
                    pass
                else:
                    Professor(hukbun=id, name=name).save()
                print("-----")

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
                              + str(page) + "&hakgwa_cd=91017&gyear=" + year + "&gwamok_name=&ghakgi=" + semester
                soup = self.get_original_data(scheduleUrl)

        '''for debuging'''
        return resultTr

    @staticmethod
    def save_course_major(year, semester, tdLists):
        """ td단위로 구성된 리스트를 DB에 저장한다. """
        for td in tdLists:
            info_object = StudentHopeCareers(
                # 년도
                year=year,
                # 학기
                semester=semester,
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
    def parse_course_detail(self, year, semester, course_num, profess_num):
        """년도와 원하는 학기를 받으면 해당 년도 학기에 열린 과목의 정보를 크롤하여 parsing 한후 리스트에 담아서 리턴한다.
        :param: year(찾고자하는 년도){2008~2018}
        :param: semester(찾고자 하는 학기) {10,20}
        :param: course_num(그 학기에 해당하는 과목번호) {1,2}
        :param: profess_num(교수 학번) {1,2}
        :return:(list)
        """
        url = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu5/wssu511s.jsp?" \
              "year=" + str(year) + \
              "&hakgi=" + str(semester) + \
              "&jojik=A1000" \
              "&gwamok_no=" + str(course_num) + \
              "&gyosu_no=" + str(profess_num) + \
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
            tdRemove = str(Lecture_method)
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

    @staticmethod
    def save_course_detail(year, semester, course_num, list):
        info_object = Subject_desription(
            year=year,
            semester=semester,
            subjectCode=course_num,
            desription=list[0]
        )
        info_object.save()

        info_object = Core_Competence(
            year=year,
            semester=semester,
            subjectCode=course_num,
            # [지식응용, 검증능력, 문제해결, 도구활용, 설계능력, 팀웍스킬, 의사전달, 영향이해, 책임의식, 자기주도]
            Knowledge_application=list[1][0],
            verification_ability=list[1][1],
            problem_solving=list[1][2],
            tool_utilization=list[1][3],
            design_ability=list[1][4],
            teamwork_skill=list[1][5],
            communication=list[1][6],
            understanding_of_influence=list[1][7],
            responsibility=list[1][8]

        )
        info_object.save()
        for i in list[2]:
            info_object = Learning_Objectives(
                year=year,
                semester=semester,
                subjectCode=course_num,
                Core_competencies=i[0],
                detailed_core_competencies=i[1],
                reflectance=i[2],
                learning_objectives=i[3],
                performance_criteria=i[4],
                achievement_goals=i[5],
                evaluation_methods=i[6],
            )
            info_object.save()

        info_object = Lecture_method(
            year=year,
            semester=semester,
            subjectCode=course_num,
            # [강의형태, 수업방식, 교육용기자재]
            Lecture_type=list[3][0],
            teaching_method=list[3][1],
            educational_equipment=list[3][2]
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
            final_exam=list[5][1],
            attendance=list[5][2],
            assignments_and_others=list[5][3],
            grading_division=list[5][4]
        )
        info_object.save()
        for i in list[6]:
            info_object = Weekly_course_contents(
                year=year,
                semester=semester,
                subjectCode=course_num,

                week=i[0],
                contents=i[1],
                methods=i[2],
                related_materials=i[3],
                assignments=i[4]
            )
            info_object.save()

        info_object = Book(
            year=year,
            semester=semester,
            subjectCode=course_num,
            title=list[7][0],
            author=list[7][1],
            publisher=list[7][2],
            year_of_publication=list[7][3],
        )
        info_object.save()
