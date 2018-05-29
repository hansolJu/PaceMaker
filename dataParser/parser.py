import re

import requests
from bs4 import BeautifulSoup

from dataParser.models import *


class KutisParser(object):
    """Parse something from table of kutis website."""

    def __init__(self, user_id, user_pw):
        print("Parser 객체 생성,", user_id, user_pw)
        self.s = self.login(user_id, user_pw)

    # 로그인후 섹션 반환
    @staticmethod
    def login(user_id, user_pw):
        print("Login 페이지 접속")
        LOGIN_URL = 'https://kutis.kyonggi.ac.kr/webkutis/view/hs/wslogin/loginCheck.jsp?'
        LOGIN_DATA = {'id': user_id, 'pw': user_pw}
        with requests.Session() as s:
            res = s.post(LOGIN_URL, data=LOGIN_DATA, verify=False, allow_redirects=False)
            return s

    # 페이지 크롤
    @staticmethod
    def get_original_data(url, s):
        "Get source from web and returns BeautifulSoup object."
        html = s.get(url).text
        return BeautifulSoup(html, "html.parser")

    # String을 int형으로 반환
    @staticmethod
    def parse_string_to_int(duration, default=0):
        """Try to parse string to int, or return default value."""
        try:
            return int(duration)
        except ValueError:
            return default

    # <%Something%> 테그와 함께 테크안 모두 삭제 
    @staticmethod
    def remove_html_tags(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    # line feed 제거.
    @staticmethod
    def remove_line_feed(str_oneline):
        tmp = str_oneline
        tmp = tmp.replace('\xa0', "")
        tmp = tmp.replace('\n', "")
        tmp = tmp.replace('\t', "")
        tmp = tmp.replace('\r', "")
        return tmp


class StudentParser(KutisParser):
    # print("StudentParser 객체 생성")

    @staticmethod
    def save_info(parsed_data_list):
        '''학생정보를 데이터베이스에 저장
        :param:tdList : parse_info()의 리턴값. 2차원 배열로 구성되어있음.
        '''
        for table_data in parsed_data_list:
            info_object = StudentInfo(
                hukbun=table_data[1],
                # 성명 2
                username=table_data[2],
                # 주민등록번호 3
                jumin=table_data[3],
                # 한자성명 4
                # name_Hanja=infos[4],
                # 영문성명 5
                # name_English=infos[5] ,
                # 과정구분
                course=table_data[6],
                # 캠퍼스구분
                # campus=infos[7] ,
                # 주야구분
                # dayNight=infos[8] ,
                # 학적구분 9
                state=table_data[9],
                # 학적변동 10
                variance=table_data[10],
                # 졸업학점
                graduationCredit=table_data[11],
                # 전공
                major=table_data[12],
                # 지도교수
                advisor=table_data[13],
                # 학생구분 14
                # 산업체여부 15
                # 학점교류구분 16
                # 병역구분 17
                # 현 학년학기 18
                currentGrade=table_data[18],
                # 이수학기 / 편입인정학기
                compleSemester=table_data[19],
                # 조기졸업대상여부 20
                earlyGraduation=table_data[20],
                # 특기자구분 21
                # 입학구분22
                # 입학일자23
                admission=table_data[23],
                # 인증구분 24
                enginCertification=table_data[24],
                # 본인인증 25
                # 본적지주소 26
                # 거주지주소 27
                # address=td['address'],
                # # 전화번호
                # phone=td['phone'],
                # # 전자우편
                # email=td['email'] ,
                # 휴대폰 30
                # cellPhone=td['cellPhone'] ,
                # 카카오톡ID31
                # 메신저QQ32
                # blank33
                # 보호자34
                # 관계35
                # 근무지36
                # 보호자주소37
                # 보호자전화번호38
                # parentsPhone=td['parentsPhone']
                # 취미39
                # 특기40
                # 혈액형41
            )
            info_object.save()

    @staticmethod
    def save_grade(hukbun, parsed_data_list):
        """ 저장이나 업데이트를 위한 오브젝트 리스트를 만들어 객체리스트 리턴
        :param  hukbun: 저장할 학생의 학번 타입은 str ex)"20100000"
        :param parsed_data_list: parse_grade()의 리턴값 , 이차원 배열
        """
        # 저장하기전에 학번의 성적을 다 지운다.
        StudentGrade.objects.filter(hukbun_id=hukbun).delete()
        for table_data in parsed_data_list:
            grade_object = StudentGrade(
                hukbun_id=hukbun,
                # 이수구분
                eisu=table_data[0],
                # 인증구분
                certification=table_data[1],
                # 년도학기
                yearNsemester=table_data[2],
                # 학수코드
                subject_code=table_data[3],
                # 교과목명
                subject=table_data[4],
                # 학점
                score=int(table_data[5]),
                # 설계학점
                grade_design=(table_data[6]),
                # 등급
                grade=table_data[7],
                # 유효구분
                valid=table_data[8]
            )
            grade_object.save()

    @staticmethod
    def save_hope(hukbun, parsed_data_list):
        """ td단위로 구성된 리스트를 DB에 저장한다. """
        StudentHopeCareers.objects.filter(hukbun_id=hukbun).delete()
        for table_data in parsed_data_list:
            hope_object = StudentHopeCareers(
                hukbun_id=hukbun,
                # 진로구분
                careers=table_data[0],
                # 지망순위
                ranking=table_data[1],
                # 지망순위
                # 직업(소분류)
                job=table_data[3],
                # 희망기업
                Enterprise=table_data[4],
                # 희망연봉
                Salary=table_data[5],
                # 희망근무지역
                Address=table_data[6]
            )
            hope_object.save()

    def parse_info(self):
        """
        학생정보를 parse 후 dict object에 담아 리턴한다.
        :return: infos(dict Object)
        """
        print("학생정보 파싱 시작")

        studentInfoUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj111s.jsp?' \
                         'submenu=1&m_menu=wsco1s02&s_menu=wshj111s'
        soup = self.get_original_data(studentInfoUrl, self.s)

        result_parsing_th = []
        result_parsing_td = []
        result = []

        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:
            tds = table.findAll("td")
            ths = table.findAll("th")

            for th in ths:
                removeTag = KutisParser.remove_html_tags(str(th))
                result_parsing_th.append(removeTag)

            for td in tds:
                tmp = KutisParser.remove_html_tags(str(td))
                tmp = self.remove_line_feed(tmp)
                tmp = tmp.replace('변동내역', "")
                tmp = tmp.replace('※ 본인인증은 개인정보 변경에서 하시기 바랍니다.', "")
                result_parsing_td.append(tmp)

            result.append(result_parsing_td)
        '''for debug'''
        print("result: ", result)
        return result

    def parse_grade(self):
        """
        parse grade data, and return tds_list Object.
        :return: result--> listObject
        """
        studentgradeUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssj1/wssj170s.jsp?submenu=2'
        soup = self.get_original_data(studentgradeUrl, self.s)

        result = []

        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:
            # tr로 분리
            trs = table.findAll("tr")
            # th와 td로 분리
            for tr in trs:
                ths = tr.findAll("th")
                parsed_table_header = []  # for문 안에서 사용후 제거.
                for th in ths:
                    remove_tag = self.remove_html_tags(str(th))
                    parsed_table_header.append(remove_tag)
                tds = tr.findAll("td")
                parsed_table_data = []  # for문 안에서 사용후 제거.
                for td in tds:
                    tmp = self.remove_html_tags(str(td))
                    tmp = self.remove_line_feed(tmp)
                    tmp = tmp.replace('변동내역', "")
                    parsed_table_data.append(tmp)
                if parsed_table_data:
                    if '이수구분별' in parsed_table_data[0]:
                        findIndex = result.__len__()
                        # print(findIndex,result)
                        index_tmp = 0
                        tmp = ''
                        for i in range(findIndex, 0, -1):
                            if result[i - 1].__len__() == 9:
                                index_tmp = i
                                tmp = result[i - 1][0]
                                # print("복사할 정보",tmp,index_tmp)
                                break

                        for i in range(findIndex, index_tmp, -1):
                            if result[i - 1].__len__() == 8:
                                result[i - 1].insert(0, tmp)
                                # print(result[i-1])
                    elif parsed_table_data.__len__() < 3:
                        pass
                    else:
                        result.append(parsed_table_data)
        # print(parsed_table_header)
        print(result)
        return result

    def parse_hope(self):
        """
        parse Hope data, and return tds_list Object.
        :return: result--> listObject
        """
        studentHopeCareersUrl = 'http://kutis.kyonggi.ac.kr/webkutis/view/hs/wshj1/wshj190s.jsp?' \
                                'm_menu=wsco1s02&s_menu=wshj190s'
        soup = self.get_original_data(studentHopeCareersUrl, self.s)

        result = []

        tables = soup.findAll("table", {'class': 'list06'})
        for table in tables:

            ths = table.findAll("th")
            parsed_table_header = []  # for문안에서 사용후 제거.
            for th in ths:
                tmp = KutisParser.remove_html_tags(str(th))
                parsed_table_header.append(tmp)

            tds = table.findAll("td")
            parsed_table_data = []  # for문안에서 사용후 제거.
            for td in tds:
                tmp = KutisParser.remove_html_tags(str(td))
                tmp = self.remove_line_feed(tmp)
                tmp = tmp.replace('변동내역', "")
                parsed_table_data.append(tmp)

            # resultTd에 아무정보 없으면 저장X(Th 단 걸러내기)
            if parsed_table_data:
                pass
            else:
                result.append(parsed_table_data)

        return result


class ServerParser(KutisParser):
    """Crawing 학기 수강가능과목 and parse data """

    @staticmethod
    def save_course_major(year, semester, parsed_data_list):
        """ td 단위로 구성된 리스트를 DB에 저장한다. """
        Course.objects.filter(year=year,semester = semester).delete()
        for table_data in parsed_data_list:
            course_object = Course(
                # 년도
                year=year,
                # 학기
                semester=semester,
                # 과목번호
                subjectCode=table_data[0],
                # 과목이름
                subjectName=table_data[1],
                # 추천학년(학교에서)
                grade=table_data[2],
                # 이수구분
                eisu=table_data[3],
                # 학점
                score=table_data[4],
                # 담당교수
                professor=table_data[5],
                # 비고
                remarks=table_data[6],
                # 교시
                time=table_data[7],
                # 강의실
                lectureRoom=table_data[8]
            )
            course_object.save()

    @staticmethod
    def save_course_detail(course_id, parsed_data_list):
        # table[0] 교과목 해설
        desription_object = Subject_desription(
            course_id=course_id,
            desription=parsed_data_list[0]
        )
        desription_object.save()
        # table[1] 새부핵심역량 과의 관계
        Competence_object = Core_Competence(
            course_id = course_id,
            # [지식응용, 검증능력, 문제해결, 도구활용, 설계능력, 팀웍스킬, 의사전달, 영향이해, 책임의식, 자기주도]
            Knowledge_application=parsed_data_list[1][0],
            verification_ability=parsed_data_list[1][1],
            problem_solving=parsed_data_list[1][2],
            tool_utilization=parsed_data_list[1][3],
            design_ability=parsed_data_list[1][4],
            teamwork_skill=parsed_data_list[1][5],
            communication=parsed_data_list[1][6],
            understanding_of_influence=parsed_data_list[1][7],
            responsibility=parsed_data_list[1][8]

        )
        Competence_object.save()
        # table[2] 교과목 학습목표 및 평가방법
        for i in parsed_data_list[2]:
            Learning_object = Learning_Objectives(
                course_id=course_id,
                Core_competencies=i[0],
                detailed_core_competencies=i[1],
                reflectance=i[2],
                learning_objectives=i[3],
                performance_criteria=i[4],
                achievement_goals=i[5],
                evaluation_methods=i[6],
            )
            Learning_object.save()
        # table[3] 강의방법
        Lecture_object = Lecture_method(
            course_id=course_id,
            # [강의형태, 수업방식, 교육용기자재]
            Lecture_type=parsed_data_list[3][0],
            teaching_method=parsed_data_list[3][1],
            educational_equipment=parsed_data_list[3][2]
        )
        Lecture_object.save()
        # table[4] 과제물
        Assignment_object = Assignment(
            course_id=course_id,
            Assignment=parsed_data_list[4]
        )
        Assignment_object.save()
        # table[5] 성적 구성비율
        ratio_object = School_composition_ratio(
            course_id=course_id,
            Midterm_exam=parsed_data_list[5][0],
            final_exam=parsed_data_list[5][1],
            attendance=parsed_data_list[5][2],
            assignments_and_others=parsed_data_list[5][3],
            grading_division=parsed_data_list[5][4]
        )
        ratio_object.save()
        # table[6] 주별 강좌내용
        for i in parsed_data_list[6]:
            Weekly_object = Weekly_course_contents(
                course_id=course_id,

                week=i[0],
                contents=i[1],
                methods=i[2],
                related_materials=i[3],
                assignments=i[4]
            )
            Weekly_object.save()
        # table[7] 책
        Book_object = Book(
            course_id=course_id,
            title=parsed_data_list[7][0],
            author=parsed_data_list[7][1],
            publisher=parsed_data_list[7][2],
            year_of_publication=parsed_data_list[7][3],
        )
        Book_object.save()

    def parse_course_major(self, year, semester):
        """년도와 원하는 학기를 받으면 해당 년도 학기에 열린 과목의 정보를 크롤하여 parse한후 리스트에 담아서 리턴한다.
        :param: year(찾고자하는 년도){2009~2018}
        :param: semester(찾고자 하는 학기) {1학기:10,2학기:20}
        :return:(list)
        """
        # 년도
        year = str(year)
        # 학기
        if semester == 10:
            semester = str(10)
        elif semester == 20:
            semester = str(20)
        else:
            print("학기 오류 1학기로 초기화")
            semester = str(10)
        # 페이지
        page = 1

        scheduleUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp?" \
                      "curPage=" + str(page) + \
                      "&hakgwa_cd=91017&gyear=" + year + \
                      "&gwamok_name=&ghakgi=" + semester

        soup = self.get_original_data(scheduleUrl, self.s)

        # 최대페이지 추적
        pages = str(soup.findAll("p", {'class': 'fr'}))
        try:
            totalpage = int(re.findall('\d+', pages)[0])
        except IndexError:
            return None

        # 교수 학번 추적 후 디비 저장
        tds = soup.findAll("td")
        for td in tds:
            if "detailView_gyosu" in str(td):
                tmp = self.remove_html_tags(str(td))
                name = tmp.split("\r")[0]

                spans = td.findAll("span")[1]
                id = str(spans).split("\'")[3]

                # 하드코딩 디비저장
                Professor(hukbun=id, name=name).save()
                print("-----")

        # 파싱 시작.
        parsed_table_header = []
        result = []
        while True:
            tables = soup.findAll("table", {'class': 'list02'})
            for table in tables:
                trs = table.findAll("tr")
                for tr in trs:
                    # 같은내용 두번수행 방지
                    if parsed_table_header:
                        pass
                    else:
                        ths = tr.findAll("th")
                        for th in ths:
                            tmp = self.remove_html_tags(str(th))
                            parsed_table_header.append(tmp)

                    tds = tr.findAll("td")
                    parsed_table_data = []
                    for td in tds:
                        tmp = self.remove_html_tags(str(td))
                        tmp = self.remove_line_feed(tmp)
                        tmp = tmp.replace('       보기', "")
                        tmp = tmp.replace('보기', "")
                        parsed_table_data.append(tmp)
                    # resultTd에 아무정보 없으면 저장X(Th 단 걸러내기)
                    if parsed_table_data:
                        result.append(parsed_table_data)
                    else:
                        pass

            # 다른 페이지도 크롤링
            if page >= totalpage:
                break
            else:
                page += 1
                scheduleUrl = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp?curPage=" \
                              + str(page) + "&hakgwa_cd=91017&gyear=" + year + "&gwamok_name=&ghakgi=" + semester
                soup = self.get_original_data(scheduleUrl, self.s)

        print("course result: ", result)
        return result

    # course_num = 그학기에 해당하는 과목번호
    def parse_course_detail(self, year, semester, course_num, profess_num):
        """년도와 원하는 학기를 받으면 해당 년도 학기에 열린 과목의 정보를 크롤하여 parsing 한후 리스트에 담아서 리턴한다.
        :param: year(찾고자하는 년도){2008~2018}
        :param: semester(찾고자 하는 학기) {10,20}
        :param: course_num(그 학기에 해당하는 과목번호) ex>{A1199}
        :param: profess_num(교수 학번) ex>{20140000}
        :return:(list)
        """
        url = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu5/wssu511s.jsp?" \
              "year=" + str(year) + \
              "&hakgi=" + str(semester) + \
              "&jojik=A1000" \
              "&gwamok_no=" + str(course_num) + \
              "&gyosu_no=" + str(profess_num) + \
              "&gwajung=1"
        test = "http://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu5/wssu511s.jsp?" \
               "year=2018" \
               "&hakgi=10" \
               "&jojik=A1000" \
               "&gwamok_no=1199" \
               "&gyosu_no=20100118" \
               "&gwajung=1"
        soup = self.get_original_data(test , self.s)

        result = []
        tables = soup.findAll("table", {'class': 'list06'})
        # table[1] 교과목 해설
        description_tableheader = self.remove_html_tags(str(tables[1].findAll("th")))
        description_table_data = self.remove_html_tags(str(tables[1].findAll("td")[0]))
        result.append(description_table_data)

        print(description_tableheader)
        print(description_table_data)
        print("----------------")

        # table[2] 새부핵심역량 과의 관계
        competencies_table_header = self.remove_html_tags(str(tables[2].findAll("th")))
        competencies_parsed_list = []

        competencies_table_data = tables[2].findAll("td")
        for td in competencies_table_data:
            competencies_parsed_list.append(self.remove_html_tags(str(td)))
        result.append(competencies_parsed_list)
        print(competencies_table_header)
        print(competencies_parsed_list)
        print("----------------")

        # table[3] 교과목 학습목표 및 평가방법 td 갯수세기
        evaluation_table_headers = self.remove_html_tags(str(tables[3].findAll("th")))
        evaluation_table_rows = tables[3].findAll("tr")

        attribute_data = ''
        is_attribute = False
        count_attrib_trs = 0

        evaluation_parsed_list = []

        for table_data_lists in evaluation_table_rows:
            parsed_table_data = []
            # 핵심역량 attribute_data 을 추가.
            if is_attribute:
                parsed_table_data.append(attribute_data)
                count_attrib_trs -= 1

            table_data_lists = table_data_lists.findAll("td")
            for td in table_data_lists:
                # 핵심역량 attribute_data 값인지 판별한후, 맞으면 리스트에 삽입, 몇번해야할지 저장
                if 'rowspan' in str(td):
                    attribute_data = self.remove_html_tags(str(td))
                    count_attrib_trs = int(re.findall('\d+', str(td))[0]) - 1
                parsed_table_data.append(self.remove_line_feed(self.remove_html_tags(str(td))))
                # print("result td :",parsed_table_data)

            if parsed_table_data:
                evaluation_parsed_list.append(parsed_table_data)

            # 핵심역량을 몇번 출력할지 확인
            if count_attrib_trs != 0:
                is_attribute = True
            else:
                is_attribute = False
                attribute_data = ''

        result.append(evaluation_parsed_list)

        print(evaluation_table_headers)
        print(evaluation_parsed_list)
        print("----------------")

        # table[4] 강의방법 <input 으로 split 후 'checked'을 포함하는지 확인후, 테그삭제후 리턴
        table_header = self.remove_html_tags(str(tables[4].findAll("th")))
        print(table_header)

        table_data_list = tables[4].findAll("td")
        parsed_data_list = []
        for table_data in table_data_list:
            tmp = str(table_data)
            tmp = self.remove_line_feed(tmp)

            # 체크된 데이터만 분리
            tmp = tmp.split('<input')
            for i in tmp:
                if 'checked' in i:
                    i = '<input' + i
                    i = self.remove_html_tags(i)
                    parsed_data_list.append(i)

        result.append(parsed_data_list)
        print(parsed_data_list)
        print("------------------")

        # table[5] 과제물
        table_header = self.remove_html_tags(str(tables[5].findAll("th")))
        table_data = self.remove_html_tags(str(tables[5].findAll("td")[0]))
        result.append(table_data)

        print(table_header)
        print(table_data)
        print("----------------")

        # table[6] 성적 구성비율 존나 머리 안돌아가서 하드코딩되있음.
        table_data = self.remove_html_tags(str(tables[6].findAll("td"))
                                           .replace('\n', "")
                                           .replace("\t", "")
                                           .replace("\xa0", ""))
        tmp_list = table_data.replace('[', "").replace(']', "").split(",")

        tableheader = []
        table_data = []
        for i in tmp_list:
            th_td = i.split(" ")
            if th_td.__len__() > 2:
                tableheader.append(th_td[0] + th_td[1] + th_td[2])
                table_data.append(th_td[3])

                tableheader.append(th_td[5])
                table_data.append(th_td[7])
            else:
                tableheader.append(th_td[0])
                table_data.append(th_td[1])
        result.append(table_data)
        print(tableheader)
        print(table_data)
        print("----------------")

        # table[7] 주별 강좌내용
        table_header = self.remove_html_tags(str(tables[7].findAll("th")))
        Contents_table_rows = tables[7].findAll("tr")
        Content_parsed_data = []
        for table_data_lists in Contents_table_rows:
            parsed_table_data = []
            table_data_lists = table_data_lists.findAll("td")
            for table_data in table_data_lists:
                parsed_table_data.append(
                    self.remove_html_tags(str(table_data)).replace('\n', "").replace("\t", "").replace("\xa0", ""))
                # print("result td :",parsed_table_data)
            if parsed_table_data:
                Content_parsed_data.append(parsed_table_data)

        result.append(Content_parsed_data)
        print(table_header)
        print(Content_parsed_data)

        print("----------------")

        # table[8] 책
        book_table_header = self.remove_html_tags((str)(tables[8].findAll("th")))
        book_table_datas = tables[8].findAll("td")
        book_parsed_list = []
        for table_data in book_table_datas:
            book_parsed_list.append(self.remove_html_tags(str(table_data)))
        result.append(book_parsed_list)

        print(book_table_header)
        print(book_parsed_list)
        print("----------------")

        print(result)
        return result
