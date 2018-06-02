from django.http import HttpResponse

# Create your views here.
from django.views import View

from dataParser.models import StudentGrade, StudentInfo


def convert_year_semester(year_semester):
    if year_semester == '1학년 1학기':
        return 1
    elif year_semester == '1학년 2학기':
        return 2
    elif year_semester == '2학년 1학기':
        return 3
    elif year_semester == '2학년 2학기':
        return 4
    elif year_semester == '3학년 1학기':
        return 5
    elif year_semester == '3학년 2학기':
        return 6
    elif year_semester == '4학년 1학기':
        return 7
    elif year_semester == '4학년 2학기':
        return 8
    else:
        return None


eisu_2012_list = [
    # 1-1 1
    ['창의기초설계', '컴퓨터과학전공및진로탐색'],
    # 1-2 2
    ['C프로그래밍'],
    # 2-1 3
    ['컴퓨터구조', '자료구조론', '자바프로그래밍1', '이산수학', '수치계산'],
    # 2-2 4
    ['컴퓨터네트워크', '시스템소프트웨어', '계산이론', '자료구조설계', '자바프로그래밍2'],
    # 3-1 5
    ['프로그래밍언어론', '운영체제', '네트워크프로그래밍', '데이터베이스', '컴퓨터교육론', '워크플로우관리시스템'],
    # 3-2 6
    ['인공지능', '소프트웨어공학', '컴퓨터그래픽스', '웹서비스설계', '컴퓨터교재연구지도법', '분산및병렬처리', '소프트웨어공학'],
    # 4-1 7
    ['컴퓨터보안', '알고리듬', '캡스톤설계'],
    # 4-2 8
    ['컴퓨터과학특강', '컴파일러', '데이터베이스응용', '종합설계', '내장형시스템']
]
msc_list = []


class diagramBV(View):
    # 학번을 가져오는 함수
    def get_user_id(self):
        user_id = self.request.user.hukbun
        return user_id

    # 학번으로 현재 유저의 이수쳬계도를 구분
    def decision_eisu(self):
        user_id = self.get_user_id()
        user_id = user_id[0:4]
        # 16학번 이하 ---> 2012 교육과정
        if user_id < 2016:
            return 2012
        # 16학번 이수체계도
        elif user_id == 2016:
            return 2016
        # 17학번 이수체계도
        elif user_id == 2017:
            return 2017
        # 18학번이상 --> 18 이수 체계도
        elif user_id > 2017:
            return 2018
        # 오류
        else:
            return None

    # 현재 학기를 가져옴 ex> 4학년 1학기 --> 7(학기)
    def get_current_grade(self):
        s = self.get_user_id()
        current_grade = StudentInfo.objects \
            .filter(hukbun=s) \
            .values_list('currentGrade', flat=True)
        for i in current_grade:
            current_grade = i
        print(current_grade)
        return convert_year_semester(current_grade)

    # 학번으로 들은 과목을 학기순으로 정렬해서 가져옴
    def get_course_taken(self):
        result = []
        s = self.get_user_id()
        subject_list = StudentGrade.objects \
            .filter(hukbun=s) \
            .filter(valid='유효') \
            .order_by('yearNsemester') \
            .values_list('yearNsemester', flat=True) \
            .distinct()
        for i in subject_list:
            tmp = []
            taken_course = StudentGrade.objects \
                .filter(hukbun=s) \
                .filter(valid='유효') \
                .filter(yearNsemester=i) \
                .values_list('subject', flat=True)
            for j in taken_course:
                tmp.append(j)
            result.append(tmp)
        print(result)
        return result

    # 이수체계도에서 들은 과목을 제거하고 남은 리스트 반납
    def custom_eisu(self):
        # 2012 이수체계도 하드코딩함 ------고쳐야함.
        my_eisu = eisu_2012_list
        my_taken_course = self.get_course_taken()
        for c_semester in my_taken_course:
            for c_subject in c_semester:
                # c_subject를 비교하기 위해서
                for e_semester in my_eisu:
                    for e_subject in e_semester:
                        if c_subject == e_subject:
                            e_semester.remove(e_subject)
        return my_eisu

    # 과목명을 입력하면 그과목의 학점을 리턴
    def get_course_score(self, course_name):
        s = self.get_user_id()
        course_score = StudentGrade.objects \
            .filter(hukbun=s) \
            .filter(valid='유효') \
            .filter(subject=course_name) \
            .values_list('score',flat=True)
        for i in course_score:
            course_score = i
        print(course_score)
        return course_score

    # 과목명을 입력하면 그과목의 설계 학점을 리턴
    def get_course_grade_design(self,course_name):
        s = self.get_user_id()
        course_grade_design = StudentGrade.objects \
            .filter(hukbun=s) \
            .filter(valid='유효') \
            .filter(subject=course_name) \
            .values_list('grade_design', flat=True)
        for i in course_grade_design:
            course_grade_design = i
        print(course_grade_design)
        return course_grade_design

    def make_diagram_data(self):
        result = [self.get_course_taken()]
        return result

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.custom_eisu())
