from django.db import models
from dataParser.models import Course
from .models import Course as classCourse

class necessaryCourse(models.Model):
    year = models.CharField(max_length=6)
    childCourse = models.ForeignKey(classCourse, on_delete=models.CASCADE, related_name='necessary_child')
    parentCourse = models.ForeignKey(classCourse, on_delete=models.CASCADE, related_name='necessary_parent')


class promotedCourse(models.Model):
    year = models.CharField(max_length=6)
    childCourse = models.ForeignKey(classCourse, on_delete=models.CASCADE, related_name='promoted_child')
    parentCourse = models.ForeignKey(classCourse, on_delete=models.CASCADE, related_name='promoted_parent')


class Course(models.Model):
    # 년도
    year = models.CharField(max_length=15)
    # 학기
    semester = models.CharField(max_length=15)
    # 과목번호
    subjectCode = models.CharField(max_length=15)
    # 과목이름
    subjectName = models.CharField(max_length=50, blank=True, null=True)
    # 추천학년(학교에서)
    grade = models.CharField(max_length=50, blank=True, null=True)
    # 이수구분
    eisu = models.CharField(max_length=50, blank=True, null=True)
    # 학점
    score = models.CharField(max_length=50, blank=True, null=True)
    # 담당교수
    professor = models.CharField(max_length=50, blank=True, null=True)
    # 비고
    remarks = models.CharField(max_length=50, blank=True, null=True)
    # 교시
    time = models.CharField(max_length=50, blank=True, null=True)
    # 강의실
    lectureRoom = models.CharField(max_length=100, blank=True, null=True)
    # 학수코드
    huksu_code = models.CharField(max_length=50, blank=True, null=True)
    # 강의시수
    course_time = models.CharField(max_length=15, blank=True, null=True)
    # 설계시수
    design_score = models.CharField(max_length=15, blank=True, null=True, default="0")

    # table[1] 교과목 해설
    description = models.CharField(max_length=1000, blank=True, null=True)

    # table[2] 새부핵심역량 과의 관계
    # [지식응용, 검증능력, 문제해결, 도구활용, 설계능력, 팀웍스킬, 의사전달, 영향이해, 책임의식, 자기주도]
    Knowledge_application = models.CharField(max_length=5, blank=True, null=True)
    verification_ability = models.CharField(max_length=5, blank=True, null=True)
    problem_solving = models.CharField(max_length=5, blank=True, null=True)
    tool_utilization = models.CharField(max_length=5, blank=True, null=True)
    design_ability = models.CharField(max_length=5, blank=True, null=True)
    teamwork_skill = models.CharField(max_length=5, blank=True, null=True)
    communication = models.CharField(max_length=5, blank=True, null=True)
    understanding_of_influence = models.CharField(max_length=5, blank=True, null=True)
    responsibility = models.CharField(max_length=5, blank=True, null=True)
    self_led = models.CharField(max_length=5, blank=True, null=True)

    # # table[3] 교과목 학습목표
    # # [핵심역량, 세부핵심역량, 반영률, 학습목표, 수행준거, 성취목표, 평가방법]
    # core_competencies = models.CharField(max_length=10,blank=True, null=True)
    # detailed_core_competencies = models.CharField(max_length=10,blank=True, null=True)
    # reflectance = models.CharField(max_length=5,blank=True, null=True)
    # learning_objectives = models.CharField(max_length=200,blank=True, null=True)
    # performance_criteria = models.CharField(max_length=200,blank=True, null=True)
    # achievement_goals = models.CharField(max_length=5,blank=True, null=True)
    # evaluation_methods = models.CharField(max_length=10,blank=True, null=True)

    # table[4] 강의방법
    # [강의형태, 수업방식, 교육용기자재]
    Lecture_type = models.CharField(max_length=100, blank=True, null=True)
    teaching_method = models.CharField(max_length=100, blank=True, null=True)
    educational_equipment = models.CharField(max_length=100, blank=True, null=True)

    # table[5] 과제물
    # [과제물]
    Assignment = models.CharField(max_length=500, blank=True, null=True)

    # table[6] 성적 구성비율 존나 머리 안돌아가서 하드코딩되있음.
    # ['중간시험', '기말시험', '출석', '과제물및기타', '성적평가구분']
    Midterm_exam = models.CharField(max_length=10, blank=True, null=True)
    final_exam = models.CharField(max_length=10, blank=True, null=True)
    attendance = models.CharField(max_length=10, blank=True, null=True)
    assignments_and_others = models.CharField(max_length=10, blank=True, null=True)
    grading_division = models.CharField(max_length=10, blank=True, null=True)

    # table[7] 주별 강좌내용

    # table[8] 책
    # [도서명, 저자, 출판사, 출판년도]
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=300, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    year_of_publication = models.CharField(max_length=20, blank=True, null=True)

    # class Meta:
    #     unique_together = ('year', 'semester', 'subjectCode')

    def __str__(self):
        return self.subjectName + "\\" + self.year + "\\" + self.semester
